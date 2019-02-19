from enum import Enum

class WorkerOperation(Enum):
    #for alloy 1234
    keywordsHighlight = 1
    seedReplace = 2
    pairJudge = 3
    clipMerge = 4
    # for dextra 567
    attributeCreate = 5
    valueBind = 6
    createAndBind = 9
    focusedEntityRefinement = 7
    # for dedupe 38
    clusterReview = 8

class ERTASK(Enum):
    Cora = 1
    AbtBuy = 2
    CDdb = 3
    DblpACM = 4
    DblpScholar = 5
    Movie = 6
    Quora = 7

class TestSystems(Enum):
    DEXTRA = 1
    Alloy = 2
    Dedupe = 3
    SigirExpriment = 4


class RecordSamplingMethod(Enum):
    RandomSampling = 1
    UncertainSampling = 2
    SearchSampling = 3
    DEXTRADIDSamplingIG = 4
    DEXTRADIDSamplingIGPattern = 5
    DEXTRADIDSamplingIGPatternAttrclassifier = 6
    DEXTRADIDOfflineSamplingIGPatternAttrclassifier = 7
    DEXTRARandomSamplingIG = 8
    DEXTRARandomSamplingIGPattern = 9
    DEXTRARandomSamplingBasic = 10
    DEXTRADIDSamplingBasic = 11
    DEXTRADIDIGPatternHBF = 12
    DEXTRADIDIGPatternHBFsimple = 13
    DEXTRADIDIGPatternHBFsimple2 = 14
    DEXTRADIDIGPatternHBFsimple3 = 15
    DEXTRADIDIGPatternHBFsimple4 = 16
    hbfaffinegapOnlyclusterSimple = 17
    hbfClusterViewSimpleMinhash = 18
    hbfClusterViewSimpleMinhashaffinegap = 19
    hbfClusterViewComplexMinhashaffinegap = 20



