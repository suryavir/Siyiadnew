import core.adfisher as adfisher

site_file = 'employment.txt'
log_file = 'log.genjobs.txt'

## Collect sites from alexa

##adfisher.collect_sites_from_alexa(nsites=5, output_file=site_file, browser="firefox", alexa_link="http://www.alexa.com/topsites/category/Top/Business/Employment")

## Set up treatments

treatment1 = adfisher.Treatment("female")
treatment1.opt_in()
treatment1.set_gender("female")
treatment1.visit_sites(site_file)

treatment2 = adfisher.Treatment("male")
treatment2.opt_in()
treatment2.set_gender("male")
treatment2.visit_sites(site_file)

## Set up measurement

measurement = adfisher.Measurement()
measurement.get_ads(site='google', reloads=10, delay=5)

## Run Experiment

adfisher.run_experiment(treatments=[treatment1, treatment2], measurement=measurement, 
	agents=2, blocks=5, log_file=log_file)

## Analyze Data

## adfisher.run_ml_analysis(log_file, verbose=True)

##adfisher.run_ml_analysis(log_file="log.genjobs.txt", splitfrac=0.2, nfolds=4,feat_choice="ads", nfeat=5, verbose=False)