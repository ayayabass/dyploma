from bs4 import BeautifulSoup
book_name = "kappa"

with open(f"./aobun/{book_name}.html", "r", encoding="Shift_JIS") as file:
    soup = BeautifulSoup(file, "html.parser")

div = soup.find("div", class_="main_text")

if div:
    for rp in div.find_all("rp"):
        rp.extract()

    result_text = div.get_text(separator="").strip()

    with open(f"./aobun/{book_name}_ja_ip.txt", "w", encoding="utf-8") as output_file:
        output_file.write(result_text)

    print(f"Text has been saved to {book_name}.txt")
else:
    print("Error when extracting text")
