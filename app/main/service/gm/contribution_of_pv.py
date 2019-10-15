
class ContributionOfPV:
    HEADER_ACTUAL_VS_TARGET = (
        'NO OF PTJ',
        'TARGET PV',
        'TARGET AS OF',
        'ACTUAL AS OF',
        'VARIANCE AS OF',
        '% CONTRIBUTION'
    )

    HEADER_ACTUAL_VS_PREV_YEAR = (
        'ACTUAL AS OF',
        'ACTUAL AS OF',
        'VARIANCE'
    )

    SAMPLE_OF_CONTRIBUTION = [
        {
            "a":"NO OF PTJ",
            "b":"TARGET PV",
            "c":"TARGET AS OF",
            "d":"ACTUAL AS OF",
            "e":"VARIANCE AS OF",
            "f":"% CONTRIBUTION"
        },
        {
            "a":50,
            "b":7664016692,
            "c":4006791731,
            "d":3017433061,
            "e":"(989358671)",
            "f":"35 %"
        },
        {
            "a":100,
            "b":10132991519,
            "c":5297585882,
            "d":4144778928,
            "e":"(1152806954)",
            "f":"47 %"
        },
        {
            "a":150,
            "b":7664016692,
            "c":4006791731,
            "d":3017433061,
            "e":"(989358671)",
            "f":"56 %"
        },
        {
            "a":200,
            "b":7664016692,
            "c":4006791731,
            "d":3017433061,
            "e":"(989358671)",
            "f":"62 %"
        },
        {
            "a":300,
            "b":7664016692,
            "c":4006791731,
            "d":3017433061,
            "e":"(989358671)",
            "f":"70 %"
        },
        {
            "a":443,
            "b":7664016692,
            "c":4006791731,
            "d":3017433061,
            "e":"(989358671)",
            "f":"80 %"
        },
        {
            "a":788,
            "b":7664016692,
            "c":4006791731,
            "d":3017433061,
            "e":"(989358671)",
            "f":"90 %"
        },
        {
            "a":3668,
            "b":7664016692,
            "c":4006791731,
            "d":3017433061,
            "e":"(989358671)",
            "f":"100 %"
        }
    ]

class ContributionOfPVPerformanceUpdate(ContributionOfPV):
    def ContributionOfPVByPtj(self):
        return self.SAMPLE_OF_CONTRIBUTION

