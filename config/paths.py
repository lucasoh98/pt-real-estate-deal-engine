
from pathlib import Path


# Root directory of the project
ROOT = Path(__file__).parent.parent.absolute()  # / (project root)


########################################## Project directory names #########################################
DIR_NAME_SRC = "src"
DIR_NAME_DATA = "data"
DIR_NAME_MODELS = "models"
DIR_NAME_EXPERIMENTS = "experiments"


# Data directory levels
DIR_NAME_RAW = "00_raw"
DIR_NAME_CLEAN = "01_clean"
DIR_NAME_CURATED = "02_curated"


################################################### Paths ###################################################
DATA = ROOT.joinpath(DIR_NAME_DATA)                         # /data
RAW = DATA.joinpath(DIR_NAME_RAW)                           # /data/00_raw
CLEAN = DATA.joinpath(DIR_NAME_CLEAN)                       # /data/01_clean
CURATED = DATA.joinpath(DIR_NAME_CURATED)                   # /data/02_curated

MODELS = ROOT.joinpath(DIR_NAME_MODELS)                     # /models
EXPERIMENTS = ROOT.joinpath(DIR_NAME_EXPERIMENTS)           # /experiments


RAW_LISTINGS_FILE = RAW.joinpath("portugal_listinigs.csv")  # /data/00_raw/portugal_listinigs.csv

RAW_LISTINGS_FILE_APARTMENT = RAW.joinpath("apartment.parquet")
RAW_LISTINGS_FILE_HOUSE = RAW.joinpath("house.parquet")
RAW_LISTINGS_FILE_LAND = RAW.joinpath("land.parquet")

