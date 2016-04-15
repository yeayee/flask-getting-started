from app import create_app
#  wsigi配置环境，并准备发布到服务端
application = create_app('production')

if __name__ == '__main__':
    application.run()
