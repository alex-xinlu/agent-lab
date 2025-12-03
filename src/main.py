from dotenv import load_dotenv

from pyouter.app import App
from pyouter.router import Router

from options import get_args_parser
from config.config import load_config
from common.logger import init_log
from common.path.base import init_path


def main_dispatch():
    """ 主路由

    """

    from test import dispatch as test_dispatch

    router = Router(
        test=test_dispatch()
    )

    return router


def run():
    """ 入口函数
    
    """

    # 获取命令行参数
    args_parser = get_args_parser()
    options = args_parser.parse_args()

    # 加载配置文件
    config = load_config(options)

    app = App(
        config=config, 
        parser=args_parser
    )

    # 加载 .env 文件中的环境变量
    load_dotenv()

    print("@init log...")
    init_log(config, options)
    print("")

    print("@init data dir...")
    init_path(options)
    print("")

    app.use(
        router=Router(
            hello_agent=main_dispatch()
        )
    )

    app.run()


if __name__=="__main__":
    run()
