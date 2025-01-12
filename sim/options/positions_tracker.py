from Gaudi.Configuration import *

# Data service
from Configurables import FCCDataSvc
podioevent = FCCDataSvc("EventDataSvc")

# DD4hep geometry service
from Configurables import GeoSvc
geoservice = GeoSvc("GeoSvc", detectors=[ 'file:Detector/DetFCChhBaseline1/compact/FCChh_DectEmptyMaster.xml',
                                          'file:Detector/DetFCChhTrackerTkLayout/compact/Tracker.xml'
],
                    OutputLevel = INFO)

from Configurables import SimSvc
geantservice = SimSvc("SimSvc", detector='SimDD4hepDetector', physicslist="SimFtfpBert", actions="SimFullSimActions")

from Configurables import SimAlg, SimSaveTrackerHits
savetool = SimSaveTrackerHits("saveHits", readoutNames = ["TrackerBarrelReadout"])
savetool.positionedTrackHits.Path = "PositionedHits"
savetool.trackHits.Path = "Hits"
savetool.digiTrackHits.Path = "digiHits"
from Configurables import SimSingleParticleGeneratorTool
pgun=SimSingleParticleGeneratorTool("SimSingleParticleGeneratorTool",saveEdm=True,
                                      particleName = "mu-", energyMin = 1000, energyMax = 1000, etaMin = 0, etaMax = 0,
                                      OutputLevel = DEBUG)
geantsim = SimAlg("SimAlg",
                    outputs= ["SimSaveTrackerHits/saveHits"],
                    eventProvider = pgun,
                    OutputLevel=DEBUG)

from Configurables import CreateVolumeTrackPositions
positions = CreateVolumeTrackPositions("positions", OutputLevel = VERBOSE)
positions.hits.Path = "Hits"
positions.positionedHits.Path = "Positions"

# PODIO algorithm
from Configurables import PodioLegacyOutput
out = PodioLegacyOutput("out",
                  OutputLevel=DEBUG)
out.outputCommands = ["keep *"]
out.filename = "positions_trackerSim.root"

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
ApplicationMgr( TopAlg = [geantsim, positions, out],
                EvtSel = 'NONE',
                EvtMax   = 1,
                # order is important, as GeoSvc is needed by G4SimSvc
                ExtSvc = [podioevent, geoservice, geantservice, audsvc],
                OutputLevel=DEBUG
)
