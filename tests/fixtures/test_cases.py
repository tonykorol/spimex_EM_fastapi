from contextlib import nullcontext as does_not_raise

import pytest
from fastapi import HTTPException

# url, params, expected_status_code, expected_payload, expectation
PARAMS_TEST_TRADING_DATES_HANDLER = [
    # positive case with custom params
    (
        '/last_trading_dates/',
        {"count": 5},
        200,
        {
            "dates": [
                "2024-02-20",
                "2024-02-19",
                "2024-02-18",
                "2024-02-17",
                "2024-02-16",
            ]
        },
        does_not_raise()
    ),

    # positive case with default params
    (
        '/last_trading_dates/',
        {},
        200,
        {
            "dates": [
                "2024-02-20",
                "2024-02-19",
                "2024-02-18",
                "2024-02-17",
                "2024-02-16",
                "2024-02-15",
                "2024-02-14",
                "2024-02-13",
                "2024-02-12",
                "2024-02-11"
            ]
        },
        does_not_raise()
    ),

    # negative case with count less than 1
    (
        '/last_trading_dates/',
        {"count": -5},
        422,
        {
            "detail": [
                {
                    "type": "greater_than_equal",
                    "loc": [
                        "query",
                        "count"
                    ],
                    "msg": "Input should be greater than or equal to 1",
                    "input": "-5",
                    "ctx": {
                        "ge": 1
                    }
                }
            ]
        },
        does_not_raise()
    )
]

# url, params, expected_status_code, expectation
PARAMS_TEST_DYNAMICS_HANDLER = [

    #positive case with custom params
    (
        "/dynamics/",
        {
            "oil_id": "A10K",
            "delivery_type_id": "W",
            "delivery_basis_id": "ZLY",
            "start_date": "2024-02-10",
            "end_date": "2024-02-11",
        },
        200,
        does_not_raise()
    ),

    # positive case with default params
    (
        "/dynamics/",
        {
            "start_date": "2024-02-11",
        },
        200,
        does_not_raise()
    ),

    # negative case without params
    (
        "/dynamics/",
        {},
        422,
        does_not_raise()
    ),

    #negative case with start_date greater than end_date
    (
        "/dynamics/",
        {
            "oil_id": "A10K",
            "delivery_type_id": "W",
            "delivery_basis_id": "ZLY",
            "start_date": "2024-02-12",
            "end_date": "2024-02-11",
        },
        400,
        pytest.raises(HTTPException)
    ),

]


# url, params, expected_status_code, expectation
PARAMS_TEST_TRADING_RESULTS_HANDLER = [

    #positive case with custom params
    (
        "/trading_results/",
        {
            "oil_id": "A10K",
            "delivery_type_id": "W",
            "delivery_basis_id": "ZLY",
        },
        200,
        does_not_raise()
    ),

    # positive case with default params
    (
        "/trading_results/",
        {},
        200,
        does_not_raise()
    ),
]


