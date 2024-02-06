import json

def read_openfoam_dictionary(file_path):
    def process_value(lines_iter, line_number):
        line = lines_iter[line_number]
        line_number += 1
        if line == "{":
            value, line_number = process_block(lines_iter, line_number)
        elif line == "(":
            value, line_number = process_array(lines_iter, line_number)
        else:
            raise Exception("Invalid dictionary, expected a block or array")

        return value, line_number

    def process_block(lines_iter, line_number):
        result_dict = {}
        # Iterate over the lines in the block
        while line_number < len(lines_iter):
            line = lines_iter[line_number]
            line_number += 1
            if line == "}":
                break
            elif line.endswith(";"):
                key, value = process_line(line)
                result_dict[key] = value
            # The start of a nested block will just be a key
            elif len(line.split()) == 1:
                key = line.strip()
                value, line_number = process_value(lines_iter, line_number)
                result_dict[key] = value
        return result_dict, line_number

    def process_array(lines_iter, line_number):
        result_list = []
        while line_number < len(lines_iter):
            line = lines_iter[line_number]
            line_number += 1
            if line.startswith(")"):
                break
            elif line.startswith("("):
                result_list.append(process_inline_array(line))
            elif len(line.split()) == 1:
                key = line.strip()
                value, line_number = process_value(lines_iter, line_number)
                if isinstance(value, dict):
                    value = {key: value}
                result_list.append(value)
            elif line.endswith(";"):
                key, value = map(str.strip, line.rstrip(';').split(None, 1))
                try:
                    value = int(value)
                except ValueError:
                    try:
                        value = float(value)
                    except ValueError:
                        pass
                result_list.append(value)
            elif line.startswith("hex"):
                result_list.append(process_hex(line))
            else:
                result_list += line.split()
        return result_list, line_number

    # hex line is a special case, looks like:
    # hex (0 1 2 3 4 5 6 7) (20 20 1) simpleGrading (1 1 1)
    # which gives ['hex',[0,1,2,3,4,5,6,7],[20,20,1],'simpleGrading',[1,1,1]]
    def process_hex(line):
        result_list = ['hex']
        line = line.strip("hex")
        iter_list = iter(line.split())
        while True:
            try:
                item = next(iter_list)
                if item.startswith("("):
                    sub_list = [item.strip("(")]
                    while True:
                        try:
                            sub_item = next(iter_list)
                            if sub_item.endswith(")"):
                                sub_list.append(sub_item.strip(")"))
                                break
                            else:
                                sub_list.append(sub_item)
                        except StopIteration:
                            raise Exception("Invalid hex line, expected closing parenthesis")
                    result_list.append(sub_list)
                else:
                    result_list.append(item)
            except StopIteration:
                break
        return result_list

    def process_line(line):
        key, value = map(str.strip, line.rstrip(';').split(None, 1))

        if "uniform" in value: # For either "uniform (0 0 0)" or "uniform 0"
            uniform_value = process_inline_array(value)
            value = {"uniform": uniform_value}
        # also wanty to process the line "dimensions      [0 1 -1 0 0 0 0];"
        elif value.startswith("["):
            value = process_inline_array(value)

        else:
            try:
                value = int(value)
            except ValueError:
                try:
                    value = float(value)
                except ValueError:
                    if value == "yes":
                        value = True
                    elif value == "no":
                        value = False
                    else:
                        pass
        return key, value

    def process_inline_array(line):
        result_list = []
        line_list = line.split()
        for item in line_list:
            item = item.strip("()[]")
            try:
                item = int(item)
            except ValueError:
                try:
                    item = float(item)
                except ValueError:
                    pass
            result_list.append(item)
        return result_list

    result_dict = {}

    print(f"Reading file '{file_path}'")

    try:
        with open(file_path, 'r') as file:
            lines = file.read().splitlines()
            lines = [line.strip() for line in lines]

            CommentBlock = True

            line_number = 0
            while line_number < len(lines):
                line = lines[line_number].strip()
                line_number += 1
                if CommentBlock:
                    if line.startswith("// *"):
                        CommentBlock = False
                elif not CommentBlock:
                    if line.strip() == "":
                        continue
                    elif line.startswith("//"):
                        continue
                    elif line.endswith(";"):
                        key, value = map(str.strip, line.rstrip(';').split(None, 1))
                        # We want value to be the correcrt type, so we try to
                        # convert it to an int or float, otherwise leave it as a string
                        try:
                            value = int(value)
                        except ValueError:
                            try:
                                value = float(value)
                            except ValueError:
                                pass
                        result_dict[key] = value
                    elif len(line.split()) == 1:
                        # if the line is just a string, it's the start of a block
                        # if it is an integer, it's the start of an array of
                        # dictionaries. result_dict will be a list of dictionaries
                        if line.isdigit():
                            result_dict = []

                        else:
                            key = line.strip()
                            value, line_number = process_value(lines, line_number)
                            if isinstance(result_dict, list):
                                result_dict.append({key: value})
                            else:
                                result_dict[key] = value

    except Exception as e:
        print(f"Error parsing file '{file_path}' at line {line_number}: {str(e)}")
        print(f"Line: {line}")

    print(result_dict)
    return result_dict

def print_nested_dict(d, indent=0):
    for key, value in d.items():
        if isinstance(value, dict):
            print(f"{' ' * indent}{key}: {{")
            print_nested_dict(value, indent + 2)
            print(f"{' ' * indent}}}")
        elif isinstance(value, list):
            print(f"{' ' * indent}{key}: [")
            for item in value:
                if isinstance(item, dict):
                    print(f"{' ' * (indent + 2)}{{")
                    print_nested_dict(item, indent + 4)
                    print(f"{' ' * (indent + 2)}}},")
                else:
                    print(f"{' ' * (indent + 2)}{item},")
            print(f"{' ' * indent}]")
        else:
            print(f"{' ' * indent}{key}: {value},")
