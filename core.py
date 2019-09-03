import logging

import config


class AvaLogger:

    def __init__(self, name,
                 path,
                 mode=config.MODE,
                 format=config.FORMAT,
                 level=config.LEVEL,):

        if not path or not name:
            raise ValueError("path and name MUST be provided for log to work properly")
        if not mode.upper() in config.MODE_TYPES:
            raise ValueError("mode should be 'DEBUG' or 'PRODUCTION'")
        if not config.EXTRA['module_name']:
            config.EXTRA['module_name'] = name
        self.level = None
        self.path = None
        self.format = None
        self.mode = mode.upper()
        self.name = name
        self._set_level(level)
        self._set_format(format)
        self._set_path(path)
        self._make_logger()
        self.set_format_extra(config.EXTRA)

    def _make_logger(self):
        """make the logger object

        we will make the logger object and use it in our modules. this instanse
        will generate a logger based on the configurations provided by the
        the register method.

        if 'DEBUG' mode is selected, we will send a version or logs to std.out
         too, so logs are viewd on the console.
        """
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.INFO)

        err_handler = logging.FileHandler(self.path)
        err_handler.setLevel(self.level)
        err_handler.setFormatter(self.format)

        self.logger.addHandler(err_handler)

    def _set_level(self, level):
        """set the level for logging module

        we will recive a level from somewhere, we check if it's one of accepted
        level's of logging and set the logging level. if it's not one of the
        accepted values, we raise an error telling them we wont accept the
        level being thrown.

        accepted values are: info, debug, critical, error, warn, warning, error
        """
        if type(level) == str:
            self.level = config.LEVEL_NAMES.get(level.lower(), None)
        elif type(level) == int:
            self.level = config.LEVEL_INTS.get(level, None)
        else:
            raise ValueError("log level should be one of ['info', 'debug', 'warning', 'error', 'critical'].")

    def _set_format(self, format):
        """set logging format for the logger object

        this will recive a format string, tries to parse it and use this as the
         logging format. format could have variables like:
            %(asctime)s   human readable time of the log being recorded
            %(created)f   log record time as epoc time (time.time())
            %(filename)s  the pathname of the location log being recorded
            %(funcName)s  the function that is recording the log
            %(levelname)s log level
            %(lineno)d    line number of the file where log is being recorded
                 (if available)
            %(module)s    name of the file where the log is being recorded
            %(name)s      name of the logger recording the log
            %(pathname)s  full path of the file which is recording the log
            %(process)d   process id(if available)

        """
        if isinstance(format, logging.Formatter):
            self.format = format
        else:
            self.format = logging.Formatter(format)


    def set_format_extra(self, extra):
        """set custom formatters for format

        this will get an dict object containing the names and values of custom
         arguments in the Format.
        Usage Example:
             guess we have a format like:
                     logging.Formatter('%(asctime)s [Module: %(module_name)s]:
                      %(message)s'))
             but, there is no `module_name` variable in default format
             variables, we need it though.
             so, we create a dict:
                     extra_formatter = {'module_name': 'webui'}
             and then, we pass this dict to the `set_format_extra`:
                     ins.set_format_extra(extra_formatter)
             where ins is the name of the class instanse.
        """
        if isinstance(extra, dict):
            self.logger = logging.LoggerAdapter(self.logger, extra)
        else:
            raise ValueError("extra_format argument should be a dict")

    def _set_path(self, path):
        """ set and check the path of the logging file
        """
        self.path = path

    @classmethod
    def register_json(cls, jsonFile=''):
        """create a new instance of the class from configs

        register json will get an *.json file as input and will return an
        instance of the AvaLogger class.
        this function will need at-least a path variable, so it now's where to
         put the logs.
        """
        import json
        try:
            confs = json.load(jsonFile)
            return AvaLogger(mode=confs.get('mode', config.MODE),
                             name=confs.get('name'),
                             path=confs.get.get('path'),
                             format=confs.get('format', config.FORMAT),
                             level=confgs.get('level', config.LEVEL)
                             )
        except ValueError:
            #TODO: Add proper handling!
            raise ValueError("wrong value has been provided, data should be json object")
            return False

    @classmethod
    def register(cls, configs):
        """ register the logger with an configs dict object.

        this will recive a dict object containing some values such as `name`,
        `path`, `mode` `format` and `level`. though `name` and `path` should
        be provided or we get error. this function will return an object
        containing the logger object and is useable.
        """
        try:
            if isinstance(configs, dict):
                return AvaLogger(name=configs.get('name'),
                                 path=configs.get('path'),
                                 mode=configs.get('mode', config.MODE),
                                 format=configs.get('format', config.FORMAT),
                                 level=configs.get('level', config.LEVEL))
            else:
                raise ValueError("configs object should be a dict")
        except KeyError:
            raise KeyError("wrong settings in the file")

    def log(self, message, level='info', *args, **kwargs):
        """record a log line

        this function will get in the message, level, and some custom variables
         if needed and then records a log line in to the files.
        """
        if self.logger:
            try:
                if level == 'info':
                    self.logger.info(message)
                elif level == 'debug':
                    self.logger.debug(message)
                elif level == 'error':
                    self.logger.exception(message)
                elif level == 'warning':
                    self.logger.warning(message)
                elif level == 'critical':
                    self.logger.critical(message)
            except Exception as e:
                print str(e)
                return False
