import json


class ResponseChange:
    def __init__(self, answer: str):
        self.answer = answer
        # self.pattern = r'```([^`]*)```'
        # self.pattern = r'```json(.*?)```'
        start_marker = '```json\n'
        end_marker = '```'
        start_index = self.answer.find(start_marker) + len(start_marker)
        end_index = self.answer.find(end_marker, start_index)
        self.json_content = self.answer[start_index:end_index]
        # self.match = re.findall(self.pattern, self.answer)

    def get_parsed_json(self):
        try:
            json_data = json.loads(self.json_content)
            json_data_pattern = json_data["emotion_delta"]
            print(json_data_pattern)
            print(json.dumps(json_data_pattern, ensure_ascii=False, indent=2))
            return json_data_pattern
        except json.JSONDecodeError as e:
            raise e
