from pypdflite import PDFCursor


def TestCursor(test_dir):
    cursor1 = PDFCursor(20, 30)
    cursor2 = PDFCursor(22, 50)

    #print "Should be True:", cursor1 < cursor2
    print ("Should be False: ", cursor1 > cursor2)
    print ("Should be False: ", cursor1 == cursor2)

if __name__ == '__main__':
    TestCursor()
