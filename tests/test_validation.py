from fp.validation import Validation
from fp.option import Option
from fp.list import List
from fp import identity


def test_create_validation_from_option_empty():
    assert Validation.from_option(Option.empty(), 'err').is_failure()


def test_create_validation_from_option_non_empty():
    assert not Validation.from_option(Option.some(1), 'err').is_failure()


def test_create_validation_from_optional_empty():
    assert Validation.from_optional(None, 'err').is_failure()


def test_create_validation_from_optional_non_empty():
    assert not Validation.from_optional(1, 'err').is_failure()


def test_fold_from_option_empty():
    assert Validation \
               .from_option(Option.empty(), 'my error message') \
               .fold(identity, identity) == 'my error message'


def test_fold_from_option_non_empty():
    assert Validation \
               .from_option(Option.some(1), 'err') \
               .fold(identity, identity) == 1


# def test_validation_sequence_failure():
#     assert Validation \
#                .sequence(List(Validation.failure('a'), Validation.failure('b'), Validation.failure('c'))) \
#                .fold(lambda err: err, lambda x: x) \
#                .unwrap() == ['a', 'b', 'c']

# def test_validation_sequence_success():
#     assert Validation \
#                .sequence(List(Validation.success(1), Validation.success(2), Validation.success(3))) \
#                .fold(identity, identity) \
#                .unwrap() == [1, 2, 3]

# def test_validation_sequence_with_success_and_failure():
#     assert Validation \
#                .sequence(
#         List(Validation.success(1), Validation.failure('err1'), Validation.success(3), Validation.failure('err2'))) \
#                .fold(identity, identity) \
#                .unwrap() == ['err1', 'err2']

# def test_validation_example():
#     fn = Validation.from_option(Option(None), 'first name is empty')
#     ln = Validation.from_option(Option(None), 'last name is empty')
#     age = Validation.from_option(Option(None), 'age is empty')
#     zip = Validation.from_option(Option(None), 'zipcode is empty')
#     assert Validation.sequence(List(fn, ln, age, zip)) \
#         .fold(identity, identity) \
#         .unwrap() == ['first name is empty', 'last name is empty', 'age is empty', 'zipcode is empty']


def test_map_validation_success():
    assert Validation.success(1) \
               .map(identity).get() == 1


def test_map_validation_failure():
    assert Validation.failure('err') \
               .map(identity).get() == 'err'


def test_bind_validation_success():
    assert Validation.success(1) \
               .bind(lambda x: Validation.success(x + 1)) \
               .bind(lambda x: Validation.success(x + 1)) \
               .bind(lambda x: Validation.success(x + 1)) \
               .fold(identity, identity) == 4


def test_bind_validation_failure():
    assert Validation.failure('err') \
               .bind(lambda x: Validation.success(x + 1)) \
               .bind(lambda x: Validation.success(x + 1)) \
               .bind(lambda x: Validation.success(x + 1)) \
               .fold(identity, identity) == 'err'


def test_validation_from_try_catch_with_div_by_zero():
    res = Validation.from_try_catch(lambda: 1 / 0)
    assert res.is_failure()
    assert res.fold(lambda err: str(err),
                    lambda x: str(x)) == 'division by zero'


def test_parse_int_failure():
    assert Validation.parse_int('a').is_failure()


def test_parse_int_success():
    assert Validation.parse_int(1).is_success()


def test_parse_float_failure():
    assert Validation.parse_float('a').is_failure()


def test_parse_float_success():
    assert Validation.parse_float('1.0').is_success()


def test_parse_bool_success():
    assert Validation.parse_boolean('').is_success()
    assert Validation.parse_boolean('a').is_success()
    assert Validation.parse_boolean('0').is_success()
    assert Validation.parse_boolean('1').is_success()


from fp.list import List
from fp.option import Option


def list_clusters() -> List[str]:
    """Returns a list of cluster arns"""
    return List('arn:aws:ecs:us-east-1:0000000000:cluster/dev',
                'arn:aws:ecs:us-east-1:0000000000:cluster/test')


def list_tasks(cluster_arn: str) -> List[str]:
    """Returns a list of task arns"""
    tasks_per_cluster = {
        'arn:aws:ecs:us-east-1:0000000000:cluster/dev':
        List(
            'arn:aws:ecs:<region>:0000000000:task/c5cba4eb-5dad-405e-96db-71ef8eefe6a8'
        ),
        'arn:aws:ecs:us-east-1:0000000000:cluster/test':
        List(
            'arn:aws:ecs:<region>:0000000000:task/067ef33c-b084-44ad-8217-26512c6c7845'
        )
    }
    return Option(tasks_per_cluster.get(cluster_arn)).get_or_else(List.empty())


def describe_task(task_arn: str) -> Option[dict]:
    task_definition_per_task_arn = {
        'arn:aws:ecs:<region>:0000000000:task/c5cba4eb-5dad-405e-96db-71ef8eefe6a8':
        {
            'lastStatus': 'STOPPED'
        },
        'arn:aws:ecs:<region>:0000000000:task/067ef33c-b084-44ad-8217-26512c6c7845':
        {
            'lastStatus': 'RUNNING',
            'taskDefinitionArn': 'arn'
        }
    }
    return Option(task_definition_per_task_arn.get(task_arn))


def filter_for_running_tasks_with_task_def_arn(task: dict) -> bool:
    return Option(task.get('lastStatus')).exists(lambda x: x == 'RUNNING') \
        and Option(task.get('taskDefinitionArn')).is_defined()


def aggregate_all_tasks_for_cluster_arn() -> List[dict]:
    return list_clusters()\
        .bind(list_tasks)\
        .bind(lambda x: describe_task(x).fold(List.empty, lambda x: List(x)))\
        .filter(filter_for_running_tasks_with_task_def_arn)
