import linecache

jpn_file = open("jpn.txt", 'w', encoding='utf-8')
eng_file = open("eng.txt", 'w', encoding='utf-8')
jpn_line = "<ex_sent xml:lang=\"jpn\">"
eng_line = "<ex_sent xml:lang=\"eng\">"
line = ""
save_line = ""
i = 0
while i < 3746543:
    try:
        line = linecache.getline("examples.txt", i)
        if jpn_line in line:
            q = 24
            while line[q] != '<':
                save_line += line[q]
                q += 1
            jpn_file.write(save_line)
            jpn_file.write('\n')
            #print()
        elif eng_line in line:
            q = 24
            while line[q] != '<':
                save_line += line[q]
                #print(line[q], end='')
                q += 1
            eng_file.write(save_line)
            eng_file.write('\n')
            #print()
        save_line = ""
    except:
        save_line = ""
        i += 1
        continue
    i += 1

jpn_file.close()
eng_file.close()