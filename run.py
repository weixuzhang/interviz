from preprocess import *


################################## sparc ##################################
data_filepath = "data/sparc/dev.json"
db_path = "data/sparc/database"

examples=generate_examples_lst(data_filepath, db_path)
with open("data/sparc/examples.json", "w") as out_file:
    json.dump(examples, out_file,indent=4)

schema_examples=[sparc_add_schema(example) for example in examples]
with open("data/sparc/schema_data.json", "w", encoding="utf-8") as f:
    json.dump(schema_examples, f, ensure_ascii=False,indent=4)

interation_examples=[sparc_add_interations(example) for example in examples]
with open("data/sparc/interations_data.json", "w", encoding="utf-8") as f:
    json.dump(interation_examples, f, ensure_ascii=False,indent=4)

serialized_examples=[sparc_add_serialized_interations(example) for example in examples]
with open("data/sparc/serialized_data.json", "w", encoding="utf-8") as f:
    json.dump(serialized_examples, f, ensure_ascii=False,indent=4)

serialized_str=["interations:"+ example['interations'] +" serialized_schema:"+example['serialized_schema'] for example in serialized_examples]
with open("data/sparc/serialized_str.json", "w", encoding="utf-8") as f:
    json.dump(serialized_str, f, ensure_ascii=False,indent=4)

schema_str=["serialized_schema:"+example['serialized_schema'] for example in serialized_examples]
with open("data/sparc/schema_str.json", "w", encoding="utf-8") as f:
    json.dump(schema_str, f, ensure_ascii=False,indent=4)


print(len(examples)) # 1034


