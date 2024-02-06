import json
import pandas as pd

df = pd.read_csv(r"C:\Users\selam\IDP\Ford\HazardInsurance.csv")
Values =  []
size = 0
for index, row in df.iterrows():
    if row['ocr_doc_page_num'] == 1:
      size+=1
      y = json.loads(row['ocr_json_payload'])
      temp = []
      for x in y:
        try:
          nospace = x['key'].replace(" ","")
          low = nospace.lower()
          temp.append(low)
        except:
          pass
        try:
          nospace = x['Key'].replace(" ","")
          low = nospace.lower()
          temp.append(low)
        except:
          pass
      Values.append(temp)
template_groups = {}
alias_count = 1


for v in Values:
  template_found = None
  for template_keys in template_groups.keys():
      if any(k in template_key for k in v for template_key in template_keys):
          template_found = template_keys
          break
  if template_found:
    template_groups[template_found]["count"] += 1
  else:
    template_groups[tuple(v)] = {"count": 1}

total_objects = len(Values)
non_blank_templates = {keys: template_info for keys, template_info in template_groups.items() if keys}

sorted_templates = sorted(
    non_blank_templates.items(),
    key=lambda x: (x[1]["count"] / total_objects),
    reverse=True
)

for index, (keys, template_info) in enumerate(sorted_templates[:5], start=1):
    template_definition = ', '.join(keys)
    template_count = template_info["count"]
    template_percentage = (template_count / total_objects) * 100
    print(f"{index}. Template Name: Template {index}")
    print(f"   Count: {template_count} / {total_objects}")
    print(f"   Percentage: {template_percentage:.2f}%")
    print(f"   Definition: {template_definition}\n")