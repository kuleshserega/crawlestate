Run spiders:
    centadata
        - scrapy crawl centadata
    midlandici
        - scrapy crawl midlandici
    easyroommate
        - scrapy crawl easyroommate -a search_address='california 1'

Deploy scrapyd
    - pip install scrapyd
    - pip install scrapyd-client
    - scrapyd-deploy -L scrapyd
    - scrapyd-deploy scrapyd -p crawlestate
    - add to scrapy.cfg
        [deploy:scrapyd]
        url = http://localhost:6800/
        project = crawlestate
    - add scrapyd.conf
        [scrapyd]
        eggs_dir    = eggs
        logs_dir    = logs
        items_dir   = items
        jobs_to_keep = 5
        dbs_dir     = dbs
        max_proc    = 0
        max_proc_per_cpu = 4
        finished_to_keep = 100
        poll_interval = 5
        http_port   = 6800
        debug       = off
        runner      = scrapyd.runner
        application = scrapyd.app.application
        launcher    = scrapyd.launcher.Launcher
