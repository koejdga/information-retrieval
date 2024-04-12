from enum import Enum


class Entity:
    def __init__(self):
        self.name = ""
        self.children = []
        self.parent = None
        self.attributes = {}
        self.content = ""


class Instruction:
    def __init__(self):
        self.name = ""
        self.content = ""


class XMLParser:
    def __init__(self):
        self.root = None
        self.processing_instructions = []

    def parse(self, document):
        with open(document, 'r', encoding="utf-8") as f:
            content = [line.strip() for line in f.readlines()]

        class State(Enum):
            ENTITY = 0
            NEW_ATTRIBUTE = 1
            NEW_INSTRUCTION_NAME = 2
            END_ENTITY = 3
            END_INSTRUCTION = 4
            PROCESSING_INSTRUCTION = 5
            NEW_ENTITY_OR_INSTRUCTION_OR_END_ENTITY = 6
            ROOT_OR_INSTRUCTION = 7
            COMMENT = 8
            READ_CONTENT = 9
            NEW_INSTRUCTION_CONTENT = 10
            END_INSTRUCTION_OR_NOT = 11
            NEW_ENTITY = 12
            ATTR_ENTITY_OR_END_ENTITY = 13
            READ_ATTRIBUTE_CONTENT = 14
            ENTITY_CONTENT_OR_NOT = 15
            INSIDE_PARENTHESES_SINGLE = 16
            INSIDE_PARENTHESES_DOUBLE = 17

        current_entity = None
        current_instruction = Instruction()
        current_state = None
        current_attribute_name = ""
        for line in content:
            for char in line:
                if current_state == State.NEW_INSTRUCTION_CONTENT:
                    if char == "?":
                        current_state = State.END_INSTRUCTION_OR_NOT
                    elif char == "'":
                        current_state = State.INSIDE_PARENTHESES_SINGLE
                    elif char == '"':
                        current_state = State.INSIDE_PARENTHESES_DOUBLE
                    else:
                        current_instruction.content += char

                elif current_state == State.INSIDE_PARENTHESES_SINGLE:
                    if char == "'":
                        current_state = State.NEW_INSTRUCTION_CONTENT
                    else:
                        current_instruction.content += char

                elif current_state == State.INSIDE_PARENTHESES_DOUBLE:
                    if char == '"':
                        current_state = State.NEW_INSTRUCTION_CONTENT
                    else:
                        current_instruction.content += char

                elif current_state == State.READ_ATTRIBUTE_CONTENT:
                    if char == "'" or char == '"':
                        current_state = State.ATTR_ENTITY_OR_END_ENTITY
                        current_attribute_name = ""
                    else:
                        current_entity.attributes[current_attribute_name] += char
                        continue

                elif current_state == State.READ_CONTENT:
                    if char == "<":
                        current_state = State.NEW_ENTITY_OR_INSTRUCTION_OR_END_ENTITY
                    else:
                        current_entity.content += char
                        continue

                elif char == "?":
                    if current_state == State.NEW_ENTITY_OR_INSTRUCTION_OR_END_ENTITY \
                            or current_state == State.ROOT_OR_INSTRUCTION:
                        current_state = State.NEW_INSTRUCTION_NAME

                    elif current_state == State.NEW_ATTRIBUTE:
                        current_entity.attributes[current_attribute_name] += char

                elif char == ">":
                    if current_state == State.END_INSTRUCTION_OR_NOT:
                        current_state = State.END_INSTRUCTION
                        self.processing_instructions.append(current_instruction)
                        current_instruction = Instruction()

                    elif current_state == State.NEW_ENTITY:
                        current_state = State.ENTITY

                    elif current_state == State.END_ENTITY:
                        current_entity = current_entity.parent
                        current_state = State.ENTITY

                    elif current_state == State.ATTR_ENTITY_OR_END_ENTITY:
                        current_state = State.ENTITY

                elif current_state == State.END_INSTRUCTION_OR_NOT:
                    current_state = State.NEW_INSTRUCTION_CONTENT
                    current_instruction.content += "?" + char
                    continue

                elif char == "<":
                    if not current_entity:
                        current_state = State.ROOT_OR_INSTRUCTION
                    else:
                        current_state = State.NEW_ENTITY_OR_INSTRUCTION_OR_END_ENTITY

                elif char == "/":
                    if current_state == State.NEW_ENTITY_OR_INSTRUCTION_OR_END_ENTITY:
                        current_state = State.END_ENTITY
                    elif current_state == State.ATTR_ENTITY_OR_END_ENTITY:
                        current_state = State.NEW_ENTITY

                elif char == " ":
                    if current_state == State.NEW_ENTITY:
                        current_state = State.ATTR_ENTITY_OR_END_ENTITY
                    elif current_state == State.NEW_INSTRUCTION_NAME:
                        current_state = State.NEW_INSTRUCTION_CONTENT

                elif char == "=":
                    if current_state == State.NEW_ATTRIBUTE:
                        current_attribute_name = current_attribute_name.strip()
                        current_entity.attributes[current_attribute_name] = ""

                elif char == '"' or char == "'":
                    if current_state == State.NEW_ATTRIBUTE:
                        current_state = State.READ_ATTRIBUTE_CONTENT

                else:
                    if current_state == State.NEW_INSTRUCTION_NAME:
                        current_instruction.name += char

                    elif current_state == State.END_INSTRUCTION_OR_NOT:
                        current_instruction.content += "?" + char
                        current_state = State.NEW_INSTRUCTION_NAME

                    elif current_state == State.NEW_ENTITY:
                        current_entity.name += char

                    elif current_state == State.ROOT_OR_INSTRUCTION:
                        self.root = Entity()
                        current_entity = self.root
                        current_entity.name += char
                        current_state = State.NEW_ENTITY

                    elif current_state == State.NEW_ENTITY_OR_INSTRUCTION_OR_END_ENTITY:
                        current_state = State.NEW_ENTITY
                        entity = Entity()
                        current_entity.children.append(entity)
                        entity.parent = current_entity
                        current_entity = entity
                        current_entity.name += char

                    elif current_state == State.ATTR_ENTITY_OR_END_ENTITY:
                        current_state = State.NEW_ATTRIBUTE
                        current_attribute_name += char

                    elif current_state == State.NEW_ATTRIBUTE:
                        current_attribute_name += char

                    elif current_state == State.ENTITY:
                        current_state = State.READ_CONTENT
                        current_entity.content += char


xmlParser = XMLParser()
xmlParser.parse("testXMLdoc.xml")
