import csv
import pymorphy3

def get_part_of_speech(word, morph):
    if not word:
        return "EMPTY"
    try:
        parsed = morph.parse(word)[0]
        pos = parsed.tag.POS
        return pos if pos is not None else " "
    except Exception:
        return "ERROR"

def process_csv(input_file, output_file):
    morph = pymorphy3.MorphAnalyzer()

    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8', newline='') as outfile:

        reader = csv.reader(infile)
        writer = csv.writer(outfile)

        headers = next(reader)
        new_headers = [
            headers[0],
            'POS_arg',
            headers[1],
            headers[2],
            'POS_val'
        ]
        writer.writerow(new_headers)

        for row_num, row in enumerate(reader, 1):
            if len(row) < 3:
                print(f"в строке {row_num} недостаточно колонок: {row}")
                continue

            lfarg_raw, lffunc, lfval_raw = row
            lfarg = lfarg_raw.strip()
            lfval = lfval_raw.strip()

            pos_arg = get_part_of_speech(lfarg, morph)
            pos_val = get_part_of_speech(lfval, morph)

            writer.writerow([lfarg, pos_arg, lffunc, lfval, pos_val])


if __name__ == "__main__":
    input_filename = "lf_data_words.csv"
    output_filename = "lf_data_words_with_pos.csv"

    process_csv(input_filename, output_filename)
    print(f"готово - {output_filename}")