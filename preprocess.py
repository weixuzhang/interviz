import json
import re
import random
from third_party.spider.preprocess.get_tables import dump_db_json_schema
from third_party.miscs.bridge_content_encoder import get_database_matches
from typing import List, Dict,Union


#### generate Sparc Examples
def generate_examples_lst(data_filepath, db_path):
    """This function returns the examples in the raw (text) form."""
    with open(data_filepath, encoding="utf-8") as f:
        sparc = json.load(f)
        schema_cache = dict()
        examples = []
        for sample in sparc:
            db_id = sample["database_id"]
            if db_id not in schema_cache:
                schema_cache[db_id] = dump_db_json_schema(
                    db_path + "/" + db_id + "/" + db_id + ".sqlite", db_id
                )
            schema = schema_cache[db_id]
            example = {
                "interations":[
                    {"question": interation["utterance"],"query": interation["query"]} for interation in sample["interaction"]
                ],
                "final_question": sample["final"]["utterance"],
                "final_query": sample["final"]["query"],
                "db_id": db_id,
                "db_path": db_path,
                "db_table_names": schema["table_names_original"],
                "db_column_names": [
                    {"table_id": table_id, "column_name": column_name}
                    for table_id, column_name in schema["column_names_original"]
                ],
                "db_column_types": schema["column_types"],
                "db_primary_keys": [{"column_id": column_id} for column_id in schema["primary_keys"]],
                "db_foreign_keys": [
                    {"column_id": column_id, "other_column_id": other_column_id}
                    for column_id, other_column_id in schema["foreign_keys"]
                ],
            }
            examples.append(example)
    return examples

#### generate serialized schema
def serialize_schema(
        question: str,
        db_path: str,
        db_id: str,
        db_column_names: List[Dict[str, Union[int, str]]],
        db_table_names: List[str],
        schema_serialization_type: str = "peteshaw",
        schema_serialization_randomized: bool = False,
        schema_serialization_with_db_id: bool = True,
        schema_serialization_with_db_content: bool = False,
        normalize_query: bool = True,
) -> str:
    if schema_serialization_type == "verbose":
        db_id_str = "Database: {db_id}. "
        table_sep = ". "
        table_str = "Table: {table}. Columns: {columns}"
        column_sep = ", "
        column_str_with_values = "{column} ({values})"
        column_str_without_values = "{column}"
        value_sep = ", "
    elif schema_serialization_type == "peteshaw":
        # see https://github.com/google-research/language/blob/master/language/nqg/tasks/spider/append_schema.py#L42
        db_id_str = " | {db_id}"
        table_sep = ""
        table_str = " | {table} : {columns}"
        column_sep = " , "
        column_str_with_values = "{column} ( {values} )"
        column_str_without_values = "{column}"
        value_sep = " , "
    else:
        raise NotImplementedError

    def get_column_str(table_name: str, column_name: str) -> str:
        column_name_str = column_name.lower() if normalize_query else column_name
        if schema_serialization_with_db_content:
            matches = get_database_matches(
                question=question,
                table_name=table_name,
                column_name=column_name,
                db_path=(db_path + "/" + db_id + "/" + db_id + ".sqlite"),
            )
            if matches:
                return column_str_with_values.format(
                    column=column_name_str, values=value_sep.join(matches)
                )
            else:
                return column_str_without_values.format(column=column_name_str)
        else:
            return column_str_without_values.format(column=column_name_str)

    tables = [
        table_str.format(
            table=table_name.lower() if normalize_query else table_name,
            columns=column_sep.join(
                map(
                    lambda y: get_column_str(table_name=table_name, column_name=y["column_name"]),
                    filter(
                        lambda y: y["table_id"] == table_id,
                        db_column_names
                    ),
                )
            ),
        )
        for table_id, table_name in enumerate(db_table_names)
    ]
    if schema_serialization_randomized:
        random.shuffle(tables)
    if schema_serialization_with_db_id:
        serialized_schema = db_id_str.format(db_id=db_id) + table_sep.join(tables)
    else:
        serialized_schema = table_sep.join(tables)
    return serialized_schema


def sparc_add_schema(ex: dict) -> dict:
    questions=[interation["question"] for interation in ex["interations"]]
    queries=[interation["query"] for interation in ex["interations"]]
    serialized_schema = serialize_schema(
        question=ex["final_question"],
        db_path=ex["db_path"],
        db_id=ex["db_id"],
        db_column_names=ex["db_column_names"],
        db_table_names=ex["db_table_names"],
        schema_serialization_type="peteshaw",
        schema_serialization_randomized=False,
        schema_serialization_with_db_id=True,
        schema_serialization_with_db_content=False,
        normalize_query=True,
    )
    return {"question": questions,"queries":queries,"serialized_schema": serialized_schema}

def sparc_add_interations(ex: dict) -> dict:
    interations=[interation["question"] +" | "+interation["query"] for interation in ex["interations"]]
    serialized_schema = serialize_schema(
        question=ex["final_question"],
        db_path=ex["db_path"],
        db_id=ex["db_id"],
        db_column_names=ex["db_column_names"],
        db_table_names=ex["db_table_names"],
        schema_serialization_type="peteshaw",
        schema_serialization_randomized=False,
        schema_serialization_with_db_id=True,
        schema_serialization_with_db_content=False,
        normalize_query=True,
    )
    return {"interations": interations,"serialized_schema": serialized_schema}

def sparc_add_serialized_interations(ex: dict) -> dict:
    interations=[" | "+ interation["question"] +" | "+interation["query"] for interation in ex["interations"]]
    serialized_inter="".join(interations)
    serialized_schema = serialize_schema(
        question=ex["final_question"],
        db_path=ex["db_path"],
        db_id=ex["db_id"],
        db_column_names=ex["db_column_names"],
        db_table_names=ex["db_table_names"],
        schema_serialization_type="peteshaw",
        schema_serialization_randomized=False,
        schema_serialization_with_db_id=True,
        schema_serialization_with_db_content=False,
        normalize_query=True,
    )
    return {"interations": serialized_inter,"serialized_schema": serialized_schema}

