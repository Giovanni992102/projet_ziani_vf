import Repository
import Model
class View:
    def __init__(self, repo, model):
        self.repo = repo
        self.model = model

    def print_WACC(self, company):
        print(f"{company} WACC: \033[1m\033[31m{self.model.compute_WACC() * 100:0.2f} %\033[0m")

