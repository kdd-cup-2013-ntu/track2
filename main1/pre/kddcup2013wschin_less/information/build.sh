#!/bin/sh
perl filter.pl TW.raw More.raw > last.all
perl filter.pl Chinese.token More.token > token.all
