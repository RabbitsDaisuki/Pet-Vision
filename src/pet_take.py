import fiftyone.zoo as foz
import fiftyone as fo

dataset = foz.load_zoo_dataset(
    "coco-2017",
    splits = ["validation", "train"],
    classes = ["cat", 'dog', 'person'],
    max_samples = 1000,
)

session = fo.launch_app(dataset)