from pathlib import Path

import attr
import pylexibank


@attr.s
class CustomLexeme(pylexibank.Lexeme):
    Pages = attr.ib(default=None)


@attr.s
class CustomLanguage(pylexibank.Language):
    UltimateSource = attr.ib(default=None)
    Source = attr.ib(default=None)
    Pages = attr.ib(default=None)


class Dataset(pylexibank.Dataset):
    dir = Path(__file__).parent
    id = "barlowpacific"
    lexeme_class = CustomLexeme
    language_class = CustomLanguage

    def cmd_download(self, args):
        pass

    def cmd_makecldf(self, args):
        data = self.raw_dir.read_csv("barlowpacific.csv", dicts=True)

        concept_map = args.writer.add_concepts(id_factory=lambda c: c.gloss, lookup_factory="gloss")
        args.writer.add_languages()
        args.writer.add_sources()

        for row in pylexibank.progressbar(data):
            args.writer.add_form(
                Language_ID=row["Language_ID"],
                Parameter_ID=concept_map[row["Parameter_ID"]],
                Value=row["Form"],
                Form=row["Form"],
                Comment=row["Comment"],
                Loan=True if row["Loan"] == "TRUE" else False,
                Pages=row["Pages"],
                Source=row["Source"],
            )
