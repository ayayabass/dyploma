book_name = "yabunonaka"
output_file = open(f"./aobun/{book_name}_ua_pp.txt", "w", encoding="utf-8")
with open(f"./aobun/{book_name}_ua_ip.txt", encoding="utf-8") as book:
    for line in book:
        first = line.find("[")
        last = line.find("]")
        if first != -1:
            output = line[:first] + line[last + 1:]
            output_file.write(output)
        else:
            output_file.write(line)
output_file.close()