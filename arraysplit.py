def array_split(ary, indices_or_sections):
    '''
    Faster version of :func:`numpy.array_split`
    
    
    '''
    Ntotal = ary.shape[0]
    sub_arys = []
    A = sub_arys.append
    Nsections = len(indices_or_sections) + 1
    div_points = [0] + list(indices_or_sections) + [Ntotal]
    for i in xrange(Nsections):
        st = div_points[i]
        end = div_points[i+1]
        A(ary[st:end])
    return sub_arys
        
        
    