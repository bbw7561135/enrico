"""Central place for config file handling"""
import sys
from os.path import join
from configobj import ConfigObj, flatten_errors
from extern.configobj.validate import Validator
from environ import CONFIG_DIR


def get_config(infile, configspec=join(CONFIG_DIR, 'default.conf')):
    """Parse config file, and in addition:
    - include default options
    - exit with an error if a required option is missing"""
    config = ConfigObj(infile, configspec=configspec,
                       file_error=True)
    validator = Validator()
    # @todo: I'm not sure we always want to copy all default options here
    results = config.validate(validator, copy=True)
    if results != True:
        for (section_list, key, _) in flatten_errors(config, results):
            if key is not None:
                print('The "%s" key in the section "%s" failed validation' %
                      (key, ', '.join(section_list)))
            else:
                print('The following section was missing:%s ' %
                      ', '.join(section_list))
        print('   Please check your config file for missing '
              'and wrong options!')
        print('FATAL: Config file is not valid.')
        sys.exit(1)
    return config


# @todo: This doesn't work because missing values are invalid!!!
# Maybe fill those values by hand?
def get_default_config(configspec=join(CONFIG_DIR, 'default.conf')):
    return ConfigObj(None, configspec=configspec)


def query_config():
    import os
    """Make a new config object, asking the user for required options"""
    config = ConfigObj(indent_type='\t')
    print('Please provide the following required options [default] :')
    config['out'] = os.getcwd()
    out = raw_input('Output directory ['+config['out']+'] : ')
    if not(out=='') :
      config['out'] = out

#    Informations about the source
    config['target'] = {}
    config['target']['name'] = raw_input('Target Name : ')
    config['target']['ra'] = raw_input('Right Ascension: ')
    config['target']['dec'] = raw_input('Declination: ')
    message = ('Options are : PowerLaw, PowerLaw2, LogParabola, '
               'PLExpCutoff\nSpectral Model [PowerLaw] : ')
    config['target']['spectrum'] = 'PowerLaw'
    model = raw_input(message)
    if not(model=='') :
      config['target']['spectrum'] = model

#    informations about the ROI
    config['space'] = {}
    config['space']['xref'] = config['target']['ra']
    config['space']['yref'] = config['target']['dec']
    config['space']['rad'] = '15'
    roi = raw_input('ROI Size [15] : ')
    if not(roi=='') :
      config['space']['rad'] = roi

#    informations about the input files
    config['file'] = {}
    config['file']['spacecraft'] = config['out']+'/spacecraft.fits'
    ft2 = raw_input('FT2 file ['+config['file']['spacecraft']+'] : ')
    if not(ft2=='') :
      config['file']['spacecraft'] = ft2
    config['file']['event'] = config['out']+'/events.lis'
    ft1list = raw_input('FT1 list of files ['+config['file']['event']+'] : ')
    if not(ft1list=='') :
      config['file']['event'] = ft1list
    config['file']['xml'] = config['out']+'/'+config['target']['name']+'_'+config['target']['spectrum']+'_model.xml'
    tag = raw_input('tag [LAT_Analysis] : ')
    if not(tag=='') :
      config['file']['tag'] = tag
    else :
      config['file']['tag'] = 'LAT_Analysis'

    return get_config(config)
