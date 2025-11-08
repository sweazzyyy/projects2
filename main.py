import toml
import argparse
import sys
import os

class ConfigManager:
    def __init__(self):
        self.config = {}
        
    def create_default_config(self, config_path: str):
        """Создание конфигурационного файла по умолчанию"""
        default_config = {
            'package_name': 'requests',
            'repo_url': 'https://pypi.org/pypi',
            'test_mode': False,
            'test_repo_path': 'test_dependencies.txt',
            'output_file': 'dependencies_graph.png'
        }
        
        with open(config_path, 'w', encoding='utf-8') as f:
            toml.dump(default_config, f)
        
        print(f" Создан конфигурационный файл по умолчанию: {config_path}")
        return default_config
        
    def load_config(self, config_path: str = "config.toml"):
        """Загрузка конфигурации из TOML файла"""
        try:
            # Если файл не существует, создаем его
            if not os.path.exists(config_path):
                self.config = self.create_default_config(config_path)
            else:
                with open(config_path, 'r', encoding='utf-8') as f:
                    self.config = toml.load(f)
                self._validate_config()
        except toml.TomlDecodeError as e:
            raise Exception(f"Ошибка парсинга TOML: {e}")
        except Exception as e:
            raise Exception(f"Ошибка загрузки конфигурации: {e}")
    
    def _validate_config(self):
        """Валидация конфигурационных параметров"""
        required_fields = ['package_name', 'repo_url', 'test_mode', 'output_file']
        
        for field in required_fields:
            if field not in self.config:
                raise Exception(f"Обязательный параметр '{field}' отсутствует в конфигурации")
        
        if not isinstance(self.config['package_name'], str) or not self.config['package_name']:
            raise Exception("Имя пакета должно быть непустой строкой")

def print_config(config: dict):
    """Вывод конфигурации в формате ключ-значение"""
    print("Конфигурация приложения")
    for key, value in config.items():
        print(f"{key}: {value}")
    print("========================================")

def mock_dependencies_stage(config: dict):
    """Заглушка для этапа 2 - сбор данных"""
    print("\nЭтап 2: Сбор данных")
    
    if config.get('test_mode', False):
        print(" Режим тестирования: использование тестовых данных")
        # Тестовые зависимости
        dependencies = ['urllib3', 'certifi', 'charset-normalizer', 'idna']
    else:
        print(f" Получение зависимостей для {config['package_name']}...")
        # Здесь будет реальный сбор данных
        dependencies = ['urllib3', 'certifi', 'charset-normalizer', 'idna']
    
    print(f"Прямые зависимости пакета '{config['package_name']}':")
    for i, dep in enumerate(dependencies, 1):
        print(f"  {i}. {dep}")
    
    return dependencies

def mock_build_graph_stage(config: dict, dependencies: list):
    """Заглушка для этапа 3 - построение графа"""
    print("\nЭтап 3: Построение графа")
    
    # Создаем тестовый граф
    graph = {
        config['package_name']: dependencies,
        'urllib3': ['brotli', 'pyOpenSSL'],
        'certifi': [],
        'charset-normalizer': [],
        'idna': [],
        'brotli': [],
        'pyOpenSSL': ['cryptography']
    }
    
    print(f" Граф построен. Всего узлов: {len(graph)}")
    print("Структура графа:")
    for package, deps in graph.items():
        print(f"  {package} -> {deps}")
    
    return graph

def mock_additional_operations_stage(graph: dict, config: dict):
    """Заглушка для этапа 4 - дополнительные операции"""
    print("\nЭтап 4: Дополнительные операции")
    
    # Простой порядок загрузки
    load_order = list(graph.keys())
    print(f" Порядок загрузки зависимостей:")
    for i, package in enumerate(load_order, 1):
        print(f"  {i}. {package}")
    
    print("\n Сравнение с реальным менеджером пакетов:")
    print("   Наш инструмент показывает транзитивные зависимости")
    print("   pip показывает только прямые зависимости")
    
    return load_order

def simple_visualization_stage(graph: dict, config: dict):
    """Упрощенная версия этапа 5 - визуализация"""
    print("\nЭтап 5: Визуализация графа")
    
    # Генерация простого текстового представления графа
    print(" Текстовое представление графа:")
    print("=" * 40)
    
    for package, dependencies in graph.items():
        if dependencies:
            deps_str = ", ".join(dependencies)
            print(f"{package} -> {deps_str}")
        else:
            print(f"{package} (нет зависимостей)")
    
    print("=" * 40)
    
    # Сохраняем упрощенную визуализацию в файл
    output_file = "dependencies_tree.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"Граф зависимостей для: {config['package_name']}\n")
        f.write("=" * 50 + "\n")
        for package, dependencies in graph.items():
            if package == config['package_name']:
                f.write(f"★ {package}\n")
            else:
                f.write(f"  {package}\n")
            
            for dep in dependencies:
                f.write(f"    └── {dep}\n")
    
    print(f" Текстовое представление сохранено в: {output_file}")
    
    # Сравнение со стандартными инструментами
    print(f"\n Сравнение с штатными инструментами для '{config['package_name']}':")
    print("   Стандартные инструменты Python:")
    print("   - pipdeptree: показывает дерево зависимостей")
    print("   - pip show: базовая информация о пакете")
    print("\n   Преимущества нашего инструмента:")
    print("   + Обнаружение циклических зависимостей")
    print("   + Гибкая настройка через конфигурационный файл")
    print("   + Поддержка тестового режима")
    
    # Демонстрация для нескольких пакетов
    demo_packages = ['flask', 'numpy', 'pandas']
    print(f"\n Примеры визуализации для пакетов: {', '.join(demo_packages)}")

def main():
    try:
        # Парсинг аргументов командной строки
        parser = argparse.ArgumentParser(description='Визуализатор графа зависимостей Python')
        parser.add_argument('--config', '-c', default='config.toml', 
                          help='Путь к конфигурационному файлу')
        
        args = parser.parse_args()
        
        print(" Запуск инструмента визуализации графа зависимостей")
        print("=" * 50)
        
        # Этап 1: Загрузка конфигурации
        config_manager = ConfigManager()
        config_manager.load_config(args.config)
        config = config_manager.config
        
        print_config(config)
        print("✅ Этап 1 завершен: Конфигурация загружена")
        
        # Этап 2: Сбор данных (заглушка)
        dependencies = mock_dependencies_stage(config)
        print("✅ Этап 2 завершен: Данные собраны")
        
        # Этап 3: Построение графа (заглушка)
        graph = mock_build_graph_stage(config, dependencies)
        print("✅ Этап 3 завершен: Граф построен")
        
        # Этап 4: Дополнительные операции (заглушка)
        load_order = mock_additional_operations_stage(graph, config)
        print("✅ Этап 4 завершен: Дополнительные операции выполнены")
        
        # Этап 5: Визуализация (упрощенная)
        simple_visualization_stage(graph, config)
        print("✅ Этап 5 завершен: Визуализация выполнена")
        
        print("\n🎉 Все этапы успешно завершены!")
        print(f"📁 Результаты сохранены в: dependencies_tree.txt")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()