from Config import Control

if __name__ == '__main__':
    Control.get_logger(__name__).logger.error("出错了")
    # Control.ip_proxy.parse_page_one()