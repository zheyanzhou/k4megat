from Gaudi.Configuration import *
from Configurables import ApplicationMgr, HepMCDumper

from Configurables import GenAlg, MomentumRangeParticleGun
pgun = MomentumRangeParticleGun("PGun",
                                PdgCodes=[11], # electron
                                MomentumMin = 20, # GeV
                                MomentumMax = 20, # GeV
                                ThetaMin = 1.58, # rad
                                ThetaMax = 1.58, # rad
                                PhiMin = 0, # rad
                                PhiMax = 0) # rad
gen = GenAlg("ParticleGun", SignalProvider=pgun, VertexSmearingTool="FlatSmearVertex")
gen.hepmc.Path = "hepmc"

from Configurables import HepMCToEDMConverter
hepmc_converter = HepMCToEDMConverter("Converter")
hepmc_converter.hepmc.Path="hepmc"
hepmc_converter.genparticles.Path="allGenParticles"
hepmc_converter.genvertices.Path="allGenVertices"

from Configurables import GeoSvc
geoservice = GeoSvc("GeoSvc",  detectors=['file:Test/TestGeometry/data/Barrel_testCaloSD_rphiz.xml'],
                    OutputLevel = DEBUG)

from Configurables import SimSvc
geantservice = SimSvc("SimSvc")

from Configurables import SimAlg, SimSaveCalHits, InspectHitsCollectionsTool, SimPrimariesFromEdmTool
inspecttool = InspectHitsCollectionsTool("inspect", readoutNames=["ECalHits"], OutputLevel = INFO)
savecaltool = SimSaveCalHits("saveECalHits", readoutNames = ["ECalHits"], OutputLevel = DEBUG)
savecaltool.positionedCaloHits.Path = "positionedCaloHits"
savecaltool.caloHits.Path = "caloHits"
particle_converter = SimPrimariesFromEdmTool("EdmConverter")
geantsim = SimAlg("SimAlg", outputs= ["SimSaveCalHits/saveECalHits","InspectHitsCollectionsTool/inspect"], eventProvider=particle_converter)

from Configurables import MergeLayers
merge = MergeLayers("mergeLayers",
                    # common part of the name of the group of volumes to merge
                    volumeName = "slice",
                    # corresponding identifier in the readout for the volumes that should be merged
                    identifier = "z",
                    # readout - bitfield description from the geometry service
                    readout ="ECalHits",
                    # specify how many volumes to merge
                    # if it is a constant number (e.g. merge every second volume with previous one), 'MergeCells' can be used
                    # below: merge first 3k volumes into new one (id=0), next 10k into second one (id=1) and last 3k into third volume (id=2)
                    merge = [3000,10001,3000],
                    OutputLevel = DEBUG)
merge.inhits.Path = "caloHits"
merge.outhits.Path = "newCaloHits"

from Configurables import FCCDataSvc, PodioLegacyOutput
podiosvc = FCCDataSvc("EventDataSvc")
out = PodioLegacyOutput("out", filename="testMergeLayers.root")
out.outputCommands = ["keep *"]

ApplicationMgr(EvtSel='NONE',
               EvtMax=1,
               TopAlg=[gen, hepmc_converter, geantsim, merge, out],
               ExtSvc = [podiosvc, geoservice, geantservice,],
               OutputLevel=DEBUG)
