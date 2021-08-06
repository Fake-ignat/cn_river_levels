from fastkml import kml

# kml_dir - место, где лежит наш KML-файл

class KMLReader():
    def __init__(self, kml_dir):
        self.root = self.get_root(kml_dir)
        self.posts = self.get_posts()

    def get_root(self, kml_dir):
        # объект-контейнер для работы с KML
        k = kml.KML()

        # открываем в бинарном режиме файл и извлекаем данные в контейнер
        with open(kml_dir, 'rb') as f:
            k.from_string(f.read())

        # получаем корневой тэг
        root = list(k.features())

        # разворачиваем вложенные теги и кладем их в root пока их не дойдем дом точек
        while True:
            if len(root) < 2:
                root = list(root[0].features())
                # как получить название тэга
                tag_name = root[0].etree_element().tag.split('}')[1]
            else:
                break
        return root

    def get_posts(self):
        posts = []

        # перебираем ноды <Placemark> в папке <Folder>
        for node in self.root:
            description = node.description.split(",\n")
            cn_name, cn_river, river, critical = map(lambda x: x.split(':')[1].strip(), description)
            lon, lat = map(float, node.geometry.coords[0][:-1])

            critical = None if critical == '-,' else float(critical.replace(',', ''))

            post = {
                "name": node.name,
                "cn_name": cn_name,
                "river": river,
                "cn_river": cn_river,
                "critical": critical,
                "lon": lon,
                "lat": lat
            }
            posts.append(post)
        return posts