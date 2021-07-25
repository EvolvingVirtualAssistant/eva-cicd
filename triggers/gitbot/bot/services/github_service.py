from ghapi.all import GhApi
import re
from bot.driven.repositories import ParamsRepository


class GithubService():

    def __init__(self, params_repository: ParamsRepository):
        self._params_repository = params_repository
        pass

    def _get_pr_url_from_commit(self, repo, hash):
        api = GhApi(
            owner=self._params_repository.get_github_organization(), repo=repo)
        prs = api.search.issues_and_pull_requests(hash)

        if prs:
            for pr in prs['items']:
                html_url = pr['html_url']
                if html_url is not None and repo in html_url:
                    return html_url

        return None

    def get_pr_url_from_commit_url(self, url):
        matched_url = re.match(r".*\/commit\/.+", url)
        if matched_url is None:
            return None

        commit_split = re.split(r"\/commit\/", url)
        repo_split = commit_split[0].split("/")

        repo = repo_split[repo_split.__len__()-1]
        hash = commit_split[commit_split.__len__()-1]

        return self._get_pr_url_from_commit(repo, hash)

    def get_pr_url_from_compare_url(self, url):
        matched_url = re.match(r".*\/compare\/.+", url)
        if matched_url is None:
            return None

        compare_split = re.split(r"\/compare\/", url)
        repo_split = compare_split[0].split("/")

        repo = repo_split[repo_split.__len__()-1]
        hash = compare_split[compare_split.__len__()-1].split("...")[1]

        return self._get_pr_url_from_commit(repo, hash)
