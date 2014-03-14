import videohub
from natsort.natsort import natsorted

TITLE='Videohub Controller2.0'
HOST='172.28.127.58:9990'




def make_table_label_cur(optlist, optname, sel=0):
    TABLE_LABEL_CUR='''
    <select class="" name="###NAME###">
      ###OPTION###
    </select>
    '''
    opt=''
    for k in natsorted(optlist.keys()):
        v = optlist[k]
        if int(k) == sel:
            opt+= '<option selected="selected">'
        else:
            opt+= '<option>'
        opt+= '%d: %s' % (int(k)+1, v)
        opt+= '</option>'
    tmp=TABLE_LABEL_CUR.replace('###NAME###', optname)
    return TABLE_LABEL_CUR.replace('###OPTION###', opt)

def make_tablerow(out_labels, out_routes, in_labels):
    TABLE_ROW_TEMPLATE='''
    <tr>
        <td> ###OUT_LABEL### </td>
        <th><span class="glyphicon glyphicon-arrow-left"></span></th>
        <td> ###IN_LABEL_NEW### </td>        
        <td> ###IN_LABEL_CUR### </td>        
    </tr>
    '''
    table_row=''
    for i in range( len(out_labels) ):
        row = TABLE_ROW_TEMPLATE
        tmpstr = '%d: %s' % (i+1, out_labels[str(i)]) 
        row = row.replace('###OUT_LABEL###', tmpstr)
        
        outidx = out_routes[str(i)]
        table_sel = make_table_label_cur(in_labels, 'label', outidx)
        row = row.replace('###IN_LABEL_NEW###', table_sel)
        
        #outidx = out_routes[str(i)]
        tmpstr = '%d: %s' % (outidx+1, in_labels[ str(outidx) ]) 
        row = row.replace('###IN_LABEL_CUR###', tmpstr)
        table_row += row
    return table_row

def make_table(table_caption=''):
    TABLE_TEMPLATE='''
    <table class="table  table-striped table-condensed">
        <caption>###TABLE_CAPTION###</caption>
        <tr>
            <th>Out</th>
            <th><span class="glyphicon glyphicon-arrow-left"></span></th>
            <th>In ( New )</th>        
            <th>IN ( Current )</th>    
        </tr>
        ###TABLE_ROW###  
    </table>    
    '''
    return TABLE_TEMPLATE.replace('###TABLE_CAPTION###', table_caption)
    

def render(template, vh):
    base=''
    with open(template, 'r') as f:
        base=f.read(102400)
    base = base.replace('###TITLE###', TITLE)
    base = base.replace('###HOST###', HOST)
    
    #MAIN OUT
    table = make_table('Main Output')
    table_row = make_tablerow(vh.out_label.labels, vh.tmp_out_route.routes, vh.in_label.labels)
    table = table.replace('###TABLE_ROW###', table_row)
    base = base.replace('###TABLE_MAIN_OUT###', table)
    
    #MONITOR OUT
    table = make_table('Monitor Output')
    table_row = make_tablerow(vh.monitor_label.labels, vh.tmp_monitor_route.routes, vh.in_label.labels)
    table = table.replace('###TABLE_ROW###', table_row)
    base = base.replace('###TABLE_MONITOR_OUT###', table)
    
    
    return base


if __name__ == '__main__':
    vh = videohub.Videohub()
    vh.load_label('test.json')
    vh.load_route('test2.json')
    #DEBUG
    vh.device.video_inputs = 72
    print render('view_control.html', vh)
