class Host(object):
    def goodmorning(self):
        '''say goodmorning
        '''
        return "Good morning, %s!" % name

    if __name__ == '__main__':
        h = Host()
        hi = h.goodmorning(' zhangsan')
