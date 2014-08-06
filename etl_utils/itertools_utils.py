# -*- coding: utf-8 -*-

from .design_pattern import singleton

@singleton()
class ItertoolsUtilsClass(object):
    def split_seqs_by_size(self, seqs1, size1, inspect=False):
        """
        Combinations of split seqs by special size.

        Breadth-first version, see examples at bottom.

        Thanks @fuchaoqun for the recursion idea.
        """

        if inspect: print "[split_seqs_by_size]", seqs1, size1
        seqs_len = len(seqs1)
        assert seqs_len >= size1, "seqs1 len should greater or equal than size1."
        assert size1 > 0, "size1 should greater than zero.."
        final_result = []

        def func(seqs2, size2, pre_result2=[]):
            if inspect: print; print "pre_result2", pre_result2

            if size2 == 1: return final_result.append(pre_result2 + [seqs2])

            for idx3 in range(len(seqs2) - size2 + 1):
                idx4 = idx3 + 1
                if inspect: print ["size2", size2, "idx4", idx4]
                if inspect: print "[loop seqs2]", seqs2[:idx4], seqs2[idx4:]

                # generate a new result object
                current_result = pre_result2 + [seqs2[:idx4]]

                if len(current_result) == size1:
                    final_result.append(current_result)
                else:
                    func(seqs2[idx3+1:], size2-1, current_result)
        func(seqs1, size1)

        if inspect: print "\n"*2
        return final_result

ItertoolsUtils = ItertoolsUtilsClass()

"""
Iterator space analysis.

seqs_len,   chunk_size,   index_times
       5,            5,             1
       5,            4,             2
       5,            3,             3
       5,            2,             4
       5,            1,             1

       4,            4,             1
       4,            3,             2
       4,            2,             3
       4,            4,             1
"""
