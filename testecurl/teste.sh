#!/bin/bash

HEADER="Content-Type: application/json"

cadastro=$(cat << EOF
    {
        "name": "João da Silva",
        "email": "joao@silva.org",
        "password": "hunter2",
        "phones": [
            {
                "number": "987654321",
                "ddd": "21"
            }
        ]
    }
EOF
)

curl -X POST -d "$cadastro" "$1"