LINE_LENGTH_THRESHOLD = 150

def clean_article(article_text):
    # Cleans and reformats the article text

    # We divide the script into lines, this is to remove unnecessary whitespaces.
    lines_list = list()

    for line in article_text.split("\n"):

        # We remove whitespaces.
        stripped_line = line.strip()

        # If the line is too short we ignore it.
        if len(stripped_line) >= LINE_LENGTH_THRESHOLD:
            lines_list.append(stripped_line)

    # Now we have the article fully cleaned.
    return "   ".join(lines_list)
