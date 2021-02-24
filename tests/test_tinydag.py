from tinydag.node import Node
from tinydag.tinydag import TinyDAG


def test_tinydag():
    dag = TinyDAG(
        Node(
            name="generate_sequence",
            func=lambda: list(range(4)),
        ),
        Node(
            name="double",
            func=lambda values: [2 * x for x in values],
            depends=["generate_sequence"],
        ),
        Node(
            name="square",
            func=lambda values: [x * x for x in values],
            depends=["generate_sequence"],
        ),
        Node(
            name="sum",
            func=lambda dbs, sqs: [x + y for x, y in zip(dbs, sqs)],
            depends=["double", "square"],
        ),
    )

    dag.run(max_workers=2)
    result = dag.get_output("sum")

    assert result == [0, 3, 8, 15]
