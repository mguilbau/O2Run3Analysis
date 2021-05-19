# Authors: Laurent Aphecetche & Maxime Guilbaud           
# Contact: guilbaud@subatech.in2p3.fr                     
# 
# Simple script to create ALICE O2 analysis task core code 
#     usage: createATask.py [-h] [-j JSON]
#
# Simple exemple of JSON config file to run the script : 
# name: config.json
# {
#    "task_class": "MyDummyAnalysis",
#    "task_name": "my-dummy-analysis",
#    "outputfilename": "my_dummy_task"
# }

import sys, getopt, json
import argparse
from jinja2 import Template

## ------- Arg parser

parser = argparse.ArgumentParser(description='This script create an analysis task...')
parser.add_argument('-j', '--json', type=str, help='JSON config file for the analysis task')

args = parser.parse_args()

## ------- Read JSON

if(args.json == None) :
   infile = 'config.json'
else :
   infile = args.json

with open(infile, "r") as read_file:
    data = json.load(read_file)

## ------- Info print

print('-- This script will create your analysis task --')
print('   Config file: ' + ''   + infile)
print('      ~~> class name:'  + ' '  + data['task_class'])
print('Your task will be generated with the name: ' + data['outputfilename'] + '.cxx')

## ------- Create template

template = Template("""#include "Framework/runDataProcessing.h"
#include "Framework/runDataProcessing.h"
#include "Framework/AnalysisTask.h"
#include "Framework/AnalysisDataModel.h"
#include "Framework/ASoAHelpers.h"
#include "AnalysisDataModel/ReducedInfoTables.h"
#include "PWGDQCore/VarManager.h"
#include "PWGDQCore/HistogramManager.h"
#include "PWGDQCore/AnalysisCut.h"
#include "PWGDQCore/AnalysisCompositeCut.h"
#include "PWGDQCore/HistogramsLibrary.h"
#include "PWGDQCore/CutsLibrary.h"

using namespace o2;
using namespace o2::framework;
using namespace o2::framework::expressions;
using namespace o2::aod;

using MyEvents = o2::soa::Join<o2::aod::ReducedEvents, o2::aod::ReducedEventsExtended>;
using MyMuonTracks = soa::Join<o2::aod::ReducedMuons, o2::aod::ReducedMuonsExtra>;
    
struct {{ task_class }}  {

  void init(o2::framework::InitContext&)
  {
     //Initialize variables
  }

  void process(MyEvents::iterator const& event, MyMuonTracks const& muons)
  {
     //process something
     for (auto& muon : muons) {
    
     }
  }

};
    
o2::framework::WorkflowSpec defineDataProcessing(o2::framework::ConfigContext const& cfgc) {
   return o2::framework::WorkflowSpec{
                adaptAnalysisTask<{{ task_class }}>(cfgc)};
}
    """)

## ------- Parse arguments and write in files

with open(data['outputfilename']+'.cxx', 'w') as f:
    print(template.render(task_class=data['task_class']), file=f)

