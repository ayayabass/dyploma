from bs4 import BeautifulSoup

book_name = "kappa"
# Read the HTML file (replace 'your_file.html' with the actual file name)
with open(f"./aobun/{book_name}.html", "r", encoding="Shift_JIS") as file:
    soup = BeautifulSoup(file, "html.parser")

# Find the div with class 'main_text'
div = soup.find("div", class_="main_text")

if div:
    # Remove all rp tags and their content
    for rp in div.find_all("rp"):
        rp.extract()

    # Get the cleaned text
    result_text = div.get_text(separator="").strip()

    # Write the result to a txt file with UTF-8 encoding
    with open(f"./aobun/{book_name}_ja_ip.txt", "w", encoding="utf-8") as output_file:
        output_file.write(result_text)

    print("Text has been extracted and saved to 'output.txt'.")
else:
    print("No div with class 'main_text' found.")
