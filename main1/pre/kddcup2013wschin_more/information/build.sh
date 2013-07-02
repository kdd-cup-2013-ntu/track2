#!/bin/sh
perl filter.pl CN.raw KR.raw TW.raw More.raw > last.all
perl filter.pl Chinese.token More.token > token.all
