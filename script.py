import os
import requests

# Configurações
token = os.getenv('GITHUB_PAT')
username = "ferreira710"  # Seu username no GitHub
organization = "kabum"  # Nome da organização

# Cabeçalhos de autenticação
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github.v3+json",
}

# Função para obter os repositórios da organização
def get_org_repos():
    url = f"https://api.github.com/orgs/{organization}/repos"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

# Função para obter as contribuições em um repositório específico
def get_repo_contributions(repo_name):
    url = f"https://api.github.com/repos/{organization}/{repo_name}/contributors"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    contributors = response.json()
    for contributor in contributors:
        if contributor["login"] == username:
            return {
                "repo": repo_name,
                "commits": contributor["contributions"],
            }
    return None

# Função principal para coletar dados de todos os repositórios
def collect_org_stats():
    repos = get_org_repos()
    contributions = []

    for repo in repos:
        contrib = get_repo_contributions(repo["name"])
        if contrib:
            contributions.append(contrib)

    return contributions

# Exibindo os resultados
def print_stats(stats):
    total_commits = 0
    for stat in stats:
        total_commits += stat["commits"]
        print(f"Repositório: {stat['repo']}, Commits: {stat['commits']}")
    print(f"\nTotal de commits na organização '{organization}': {total_commits}")

# Executa o script
if __name__ == "__main__":
    stats = collect_org_stats()
    print_stats(stats)
