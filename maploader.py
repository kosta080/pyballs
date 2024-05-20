import re

class MapLoader:
    def load_svg_points(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                svg_content = file.read()
                #print("\n\n\n")
                #print(svg_content)
                #print("\n\n\n")
        except FileNotFoundError:
            print("File not found.")
            return []
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

        points = []
        pattern = r"geometry.*?x=&quot;(\d+)&quot;.*?y=&quot;(\d+)&quot;.*?x=&quot;(\d+)&quot;.*?y=&quot;(\d+)&quot;"
        matches = re.findall(pattern, svg_content)
        print(matches)
        for match in matches:
            x1, y1, x2, y2 = match
            points.append([int(x1), int(y1), int(x2), int(y2)])

        return points


