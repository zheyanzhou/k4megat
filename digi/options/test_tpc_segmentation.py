from Gaudi.Configuration import *

# geometry service
from Configurables import MegatGeoSvc as GeoSvc
from os import environ, path
detector_path = environ.get("MEGAT_ROOT", "")
geoservice = GeoSvc("MegatGeoSvc",
                    # buildType="BUILD_RECO",
                    buildType="BUILD_SIMU",
                    detectors=[path.join(detector_path, 'geometry/compact/Megat.xml'),
                                              'geometry/compact/TPC_readout.xml'],
                    OutputLevel = WARNING)

# Data service
from Configurables import k4LegacyDataSvc
datasvc = k4LegacyDataSvc("EventDataSvc")
datasvc.input = 'tpcdrift_megat.root'
# datasvc.ForceLeaves= True

# Fetch the collection into TES
from Configurables import PodioLegacyInput
inp = PodioLegacyInput()
inp.collections = ["TpcDriftHits"]

# Add algorithm
from Configurables import TpcSegmentAlg
tpcpixelseg = TpcSegmentAlg("TpcPixelSeg")
tpcpixelseg.inHits.Path = "TpcDriftHits"
tpcpixelseg.outHits.Path = "TpcSegPixelHits"
tpcpixelseg.readoutName = "TpcPixelHits"

tpcstripseg = TpcSegmentAlg("TpcStripSeg")
tpcstripseg.inHits.Path = "TpcDriftHits"
tpcstripseg.outHits.Path = "TpcSegStripHits"
tpcstripseg.readoutName = "TpcStripHits"

# Select & Write the collections to disk ROOT file
from Configurables import PodioLegacyOutput
out = PodioLegacyOutput()
out.filename = 'tpcseg_megat.root'
out.outputCommands = ['keep *']

# ApplicationMgr
from Configurables import ApplicationMgr
ApplicationMgr( TopAlg = [inp, tpcstripseg,tpcpixelseg, out],
                EvtSel = 'NONE',
                EvtMax   = -1,
                ExtSvc = [datasvc],
                OutputLevel=INFO
 )

