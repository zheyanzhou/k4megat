from Gaudi.Configuration import *

from Configurables import  HepMCFileReader, GenAlg
readertool = HepMCFileReader("Reader", Filename="Test/TestGeometry/data/testHepMCpositionsEMcal.dat")
reader = GenAlg("Reader", SignalProvider=readertool)
reader.hepmc.Path = "hepmc"

from Configurables import HepMCToEDMConverter
hepmc_converter = HepMCToEDMConverter("Converter")
hepmc_converter.hepmc.Path="hepmc"
hepmc_converter.genparticles.Path="allGenParticles"
hepmc_converter.genvertices.Path="allGenVertices"

from Configurables import HepMCDumper
hepmc_dump = HepMCDumper("hepmc")
hepmc_dump.hepmc.Path="hepmc"

# Data service
from Configurables import FCCDataSvc
podioevent = FCCDataSvc("EventDataSvc")

# DD4hep geometry service
from Configurables import GeoSvc
geoservice = GeoSvc("GeoSvc", detectors=[ 'file:Detector/DetFCChhBaseline1/compact/FCChh_DectEmptyMaster.xml',
                                          'file:Detector/DetFCChhECalInclined/compact/FCChh_ECalBarrel_withCryostat.xml'
],
                    OutputLevel = INFO)

# Geant4 service
# Configures the Geant simulation: geometry, physics list and user actions
from Configurables import SimSvc
geantservice = SimSvc("SimSvc", detector='SimDD4hepDetector', physicslist="SimTestPhysicsList", actions="SimFullSimActions")

# Geant4 algorithm
# Translates EDM to G4Event, passes the event to G4, writes out outputs via tools
# and a tool that saves the calorimeter hits
from Configurables import SimAlg, SimSaveCalHits
savetool = SimSaveCalHits("saveHits",readoutNames = ["ECalBarrelEta"])
savetool.positionedCaloHits.Path = "PositionedHits"
savetool.caloHits.Path = "Hits"

geantsim = SimAlg("SimAlg",
                       outputs= ["SimSaveCalHits/saveHits"],
                       OutputLevel=DEBUG)

from Configurables import CreateVolumeCaloPositions
positions = CreateVolumeCaloPositions("positions", OutputLevel = VERBOSE)
positions.hits.Path = "Hits"
positions.positionedHits.Path = "Positions"

# PODIO algorithm
from Configurables import PodioLegacyOutput
out = PodioLegacyOutput("out",
                   OutputLevel=DEBUG)
out.outputCommands = ["keep *"]
out.filename = "positions_ecalInclinedSim.root"

#CPU information
from Configurables import AuditorSvc, ChronoAuditor
chra = ChronoAuditor()
audsvc = AuditorSvc()
audsvc.Auditors = [chra]
geantsim.AuditExecute = True
positions.AuditExecute = True
out.AuditExecute = True

# ApplicationMgr
from Configurables import ApplicationMgr
ApplicationMgr( TopAlg = [reader, hepmc_converter, hepmc_dump, geantsim, positions, out],
                EvtSel = 'NONE',
                EvtMax   = 5,
                # order is important, as GeoSvc is needed by G4SimSvc
                ExtSvc = [podioevent, geoservice, geantservice, audsvc],
                OutputLevel=DEBUG
)
