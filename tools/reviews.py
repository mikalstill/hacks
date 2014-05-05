#!/usr/bin/python

import json

import utils


def component_reviews(component):
    cmd = ('ssh review.openstack.org gerrit query --format json '
           '--current-patch-set --all-approvals project:%s status:open '
           'limit:10000'
           % component)
    stdout = utils.runcmd(cmd)

    reviews = []
    for line in stdout.split('\n'):
        if not line:
            continue

        try:
            packet = json.loads(line)
            if packet.get('project') == component:
                reviews.append(packet)
        except ValueError as e:
            print 'Could not decode:'
            print '  %s' % line
            print '  Error: %s' % e

    return reviews

if __name__ == '__main__':
    reviews = component_reviews('openstack/nova')
    print '%s reviews found' % len(reviews)

    for review in reviews:
        print
        for key in sorted(review.keys()):
            if key == 'patchSets':
                print '%s:' % key
                for ps in review[key]:
                    print '    %s' % ps
            else:
                print '%s: %s' %(key, review[key])
