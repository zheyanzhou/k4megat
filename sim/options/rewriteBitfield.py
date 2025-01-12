from Gaudi.Configuration import *

# DD4hep geometry service
from Configurables import GeoSvc
geoservice = GeoSvc("GeoSvc", detectors=[ 'file:Detector/DetFCChhBaseline1/compact/FCChh_DectEmptyMaster.xml',
                                          'file:Detector/DetFCChhCalDiscs/compact/Endcaps_coneCryo.xml'],
                    OutputLevel = INFO)

# Geant4 service
# Configures the Geant simulation: geometry, physics list and user actions
from Configurables import SimSvc
geantservice = SimSvc("SimSvc")

# Geant4 algorithm
# Translates EDM to G4Event, passes the event to G4, writes out outputs via tools
# and a tool that saves the calorimeter hits
from Configurables import SimAlg, SimSaveCalHits
savecaltool = SimSaveCalHits("saveECalHits", readoutNames = ["EMECPhiEta"])
savecaltool.positionedCaloHits.Path = "positionedCaloHits"
savecaltool.caloHits.Path = "caloHits"
from Configurables import SimSingleParticleGeneratorTool
pgun=SimSingleParticleGeneratorTool("SimSingleParticleGeneratorTool",saveEdm=True,
                particleName="e-",energyMin=50000,energyMax=50000,etaMin=2,etaMax=2)
geantsim = SimAlg("SimAlg", outputs= ["SimSaveCalHits/saveECalHits"], eventProvider=pgun)

from Configurables import RewriteBitfield
rewrite = RewriteBitfield("Rewrite",
                          # old bitfield (readout)
                          oldReadoutName = "EMECPhiEta",
                          # specify which fields are going to be deleted
                          removeIds = ["sublayer"],
                          # new bitfield (readout), with new segmentation
                          newReadoutName = "EMECPhiEtaReco",
                          debugPrint = 10,
                          OutputLevel = DEBUG)
# clusters are needed, with deposit position and cellID in bits
rewrite.inhits.Path = "caloHits"
rewrite.outhits.Path = "caloRecoHits"

# PODIO algorithm
from Configurables import FCCDataSvc, PodioLegacyOutput
podiosvc = FCCDataSvc("EventDataSvc")
out = PodioLegacyOutput("out")
out.outputCommands = ["keep *"]
out.filename = "rewrittenBitfield_ecalEndcapSim.root"

# ApplicationMgr
from Configurables import ApplicationMgr
ApplicationMgr( TopAlg = [geantsim, rewrite, out],
                EvtSel = 'NONE',
                EvtMax   = 1,
                # order is important, as GeoSvc is needed by G4SimSvc
                ExtSvc = [podiosvc, geoservice, geantservice],
                OutputLevel=INFO)
