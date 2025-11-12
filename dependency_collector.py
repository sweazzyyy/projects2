import requests
import json
from typing import Dict, List, Set
import time

class DependencyCollector:
    def __init__(self, repo_url: str = "https://pypi.org/pypi"):
        self.repo_url = repo_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'DependencyVisualizer/1.0'
        })
    
    def get_package_info(self, package_name: str) -> Dict:
        """Получение информации о пакете из PyPI"""
        try:
            url = f"{self.repo_url}/{package_name}/json"
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Ошибка при получении информации о пакете {package_name}: {e}")
    
    def get_direct_dependencies(self, package_name: str) -> List[str]:
        """Получение прямых зависимостей пакета"""
        package_info = self.get_package_info(package_name)
        
        # Получаем последнюю версию
        latest_version = package_info['info']['version']
        
        # Ищем зависимости в информации о релизах
        dependencies = set()
        
        if latest_version in package_info.get('releases', {}):
            releases = package_info['releases'][latest_version]
            for release in releases:
                requires_dist = release.get('requires_dist', [])
                if requires_dist:
                    for dep in requires_dist:
                        # Извлекаем имя пакета (убираем версии и дополнительные условия)
                        dep_name = dep.split(' ')[0].strip()
                        if dep_name and not dep_name.startswith('python_') and dep_name != package_name:
                            dependencies.add(dep_name)
        
        # Если не нашли в релизах, проверяем в общей информации
        if not dependencies:
            requires_dist = package_info['info'].get('requires_dist', [])
            for dep in requires_dist:
                dep_name = dep.split(' ')[0].strip()
                if dep_name and not dep_name.startswith('python_') and dep_name != package_name:
                    dependencies.add(dep_name)
        
        return list(dependencies)
    
    def collect_from_test_file(self, file_path: str, package_name: str) -> List[str]:
        """Сбор зависимостей из тестового файла"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Простой парсинг тестового файла с зависимостями
            dependencies = []
            lines = content.strip().split('\n')
            
            for line in lines:
                if '->' in line:
                    parts = line.split('->')
                    if parts[0].strip() == package_name:
                        dependencies.append(parts[1].strip())
            
            return dependencies
        except Exception as e:
            raise Exception(f"Ошибка чтения тестового файла: {e}")

def collect_dependencies_stage(config: Dict) -> List[str]:
    """Этап 2: Сбор прямых зависимостей"""
    collector = DependencyCollector(config['repo_url'])
    
    if config.get('test_mode', False):
        dependencies = collector.collect_from_test_file(
            config['test_repo_path'], 
            config['package_name']
        )
    else:
        dependencies = collector.get_direct_dependencies(config['package_name'])
    
    print(f"Прямые зависимости пакета '{config['package_name']}':")
    for i, dep in enumerate(dependencies, 1):
        print(f"  {i}. {dep}")
    
    return dependencies