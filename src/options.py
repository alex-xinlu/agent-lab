from argparse import ArgumentParser
from pyouter.default import create_parser


def add_custom_arguments(parser: ArgumentParser):
    ''' 用户定制化参数选项
    
    * --cluster: 不同环境，分为 dev, uat, pro
    '''

    parser.add_argument(
        "--cluster",
        dest="cluster",
        help="Config for different environments. The default environment is 'dev'.",
        default="dev",
        nargs='?',
        type=str,
        metavar="CLUSTER"
    )

    parser.add_argument(
        "--filename",
        dest="filename",
        help="pass a filename. The default value is ''.",
        default="",
        nargs='?',
        type=str,
        metavar="FILENAME"
    )

    parser.add_argument(
        "--worker_num",
        dest="worker_num",
        help="worker_num",
        default="2",
        nargs='?',
        type=str,
        metavar="WORKER_NUM"
    )


def get_args_parser():
    parser = create_parser("hello agent")
    add_custom_arguments(parser)

    return parser


def show_help():
    """
    命令行选项说明:
    ==
    """

    help = '\n'.join([
        show_help.__doc__,
        add_custom_arguments.__doc__
    ])

    print(help)
