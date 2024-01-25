import json

def read_openfoam_dictionary(file_path):
    def process_value(lines_iter, line_number):
        if lines_iter[line_number] == "{":
            value, line_number = process_block(lines_iter, line_number)
        elif lines_iter[line_number] == "(":
            value, line_number = process_array(lines_iter, line_number)
        else:
            raise Exception("Invalid dictionary, expected a block or array")

        return value, line_number

    def process_block(lines_iter, line_number):
        result_dict = {}
        line_number += 1
        # Iterate over the lines in the block
        while line_number < len(lines_iter):
            line = lines_iter[line_number]
            if line == "}":
                line_number += 1
                break  # End of the block
            elif line.endswith(";"):
                key, value = map(str.strip, line.rstrip(';').split(None, 1))
                result_dict[key] = value
                line_number += 1
            # The start of a nested block will just be a key
            elif len(line.split()) == 1:
                line_number += 1
                key = line.strip()
                value, new_line_number = process_value(lines_iter, line_number)
                result_dict[key] = value
                line_number = new_line_number
        return result_dict, line_number

    def process_array(lines_iter, line_number):
        result_list = []
        line_number += 1
        while line_number < len(lines_iter):
            line = lines_iter[line_number]
            if line == ");":
                line_number += 1
                break  # End of the array
            elif line.startswith("("):
                result_list.append(process_inline_array(line))
                line_number += 1
            elif len(line.split()) == 1:
                line_number += 1
                key = line.strip()
                value, new_line_number = process_value(lines_iter, line_number)
                if isinstance(value, dict):
                    value = {key: value}
                result_list.append(value)
                line_number = new_line_number
            elif line.endswith(";"):
                key, value = map(str.strip, line.rstrip(';').split(None, 1))
                result_list.append(value)
                line_number += 1
            else:
                result_list += line.split()
        return result_list, line_number

    def process_inline_array(line):
        result_list = []
        line = line.strip("()")
        line_list = line.split()
        for item in line_list:
            result_list.append(item)
        return result_list

    result_dict = {}
    is_comment_block = False

    try:
        with open(file_path, 'r') as file:
            lines = file.read().splitlines()
            lines = [line.strip() for line in lines]

            line_number = 0
            while line_number < len(lines):
                line = lines[line_number]

                if line.startswith("// *"):
                    is_comment_block = False
                    line_number += 1
                    continue

                if line.startswith("/*"):
                    is_comment_block = True
                    line_number += 1
                    continue

                if not line.strip():
                    line_number += 1
                    continue

                if not is_comment_block and line.strip():
                    if line.endswith(";"):
                        key, value = map(str.strip, line.rstrip(';').split(None, 1))
                        result_dict[key] = value
                    elif len(line.split()) == 1:
                        line_number += 1
                        key = line.strip()
                        value, new_line_number = process_value(lines, line_number)
                        result_dict[key] = value
                        line_number = new_line_number

                line_number += 1
    except Exception as e:
        print(f"Error parsing file '{file_path}' at line {line_number}: {str(e)}")

    return json.dumps(result_dict)

