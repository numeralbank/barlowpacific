from pathlib import Path

import attr
import pylexibank


@attr.s
class CustomLexeme(pylexibank.Lexeme):
    Pages = attr.ib(default=None)


class Dataset(pylexibank.Dataset):
    dir = Path(__file__).parent
    id = "barlowpacific"
    lexeme_class = CustomLexeme

    # define the way in which forms should be handled
    form_spec = pylexibank.FormSpec(
        brackets={"(": ")"},  # characters that function as brackets
        separators=";/,",  # characters that split forms e.g. "a, b".
        missing_data=("?", "-"),  # characters that denote missing data.
        strip_inside_brackets=True,  # do you want data removed in brackets or not?
    )

    def cmd_download(self, args):
        pass

    def cmd_makecldf(self, args):
        data = self.raw_dir.read_csv("barlowpacific.csv", dicts=True)

        concept_map = args.writer.add_concepts(lookup_factory="gloss")
        args.writer.add_languages()
        args.writer.add_sources()

        for row in pylexibank.progressbar(data):
            args.writer.add_form(
                Language_ID=row["Glottocode"],
                Parameter_ID=concept_map[row["Numeral"]],
                Value=row["Form"],
                Form=row["Form"],
                Comment=row["Comment"],
                Loan=True if row["Loan?"] == "TRUE" else False,
                Pages=row["Pages"],
                Source=row["Source"],
            )
