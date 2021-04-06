package com.example.rasbandroid;

import android.content.Context;
import android.view.*;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.recyclerview.widget.RecyclerView;

import com.bumptech.glide.Glide;

import java.util.List;


public class RecyclerViewAdapter extends RecyclerView.Adapter<RecyclerView.ViewHolder> {
    private List<BaseMultiBean> dataList;
    private LayoutInflater inflater;
    private Context context;
    public RecyclerViewAdapter (Context context,List<BaseMultiBean>dataList) {
        this.context=context;
        this.dataList=dataList;
    }

    @Override
    public RecyclerView.ViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
        if(inflater==null){//只初始化一次
            inflater=LayoutInflater.from(parent.getContext());
        }
        switch (viewType){//根据布局类型创建合适的ViewHolder
            case BaseMultiBean.TYPE_TITLE:
                View titleView=inflater.inflate(R.layout.recycler_title,parent,false);
                return new TitleViewHolder(titleView);
            case BaseMultiBean.TYPE_ITEM:
                View itemView=inflater.inflate(R.layout.recycler_item,parent,false);
                return new ItemViewHolder(itemView);
            default:break;
        }
        return null;
    }

    @Override
    public void onBindViewHolder(RecyclerView.ViewHolder holder, int position) {
        int viewType=getItemViewType(position);
        if(viewType==BaseMultiBean.TYPE_TITLE){//为标题形式的列表项绑定数据
            TitleBean titleBean= (TitleBean) getItem(position);
            TitleViewHolder titleViewHolder= (TitleViewHolder) holder;
            titleViewHolder.titleView.setText(titleBean.getTitle());
        }
        if(viewType==BaseMultiBean.TYPE_ITEM){//为内容形式的列表项绑定数据
            ItemBean itemBean= (ItemBean) getItem(position);
            ItemViewHolder itemViewHolder= (ItemViewHolder) holder;
            Glide.with(context).load(itemBean.getImage(1)).into(itemViewHolder.itemImageView1);
            Glide.with(context).load(itemBean.getImage(2)).into(itemViewHolder.itemImageView2);
            Glide.with(context).load(itemBean.getImage(3)).into(itemViewHolder.itemImageView3);
        }
    }
    private BaseMultiBean getItem(int position){
        return dataList.get(position);
    }
    @Override
    public int getItemCount() {
        return dataList.size();
    }

    @Override
    public int getItemViewType(int position) {
        BaseMultiBean baseMultiBean=dataList.get(position);
        return baseMultiBean.getType();
    }

    //内容Item的ViewHolder
    static class ItemViewHolder extends RecyclerView.ViewHolder{
        private ImageView itemImageView1;
        private ImageView itemImageView2;
        private ImageView itemImageView3;
        public ItemViewHolder(View itemView) {
            super(itemView);
            itemImageView1=itemView.findViewById(R.id.item_image1);
            itemImageView2=itemView.findViewById(R.id.item_image2);
            itemImageView3=itemView.findViewById(R.id.item_image3);

        }
    }

    //标题Item的ViewHolder
    static class TitleViewHolder extends RecyclerView.ViewHolder{
        private TextView titleView;
        public TitleViewHolder(View itemView) {
            super(itemView);
            titleView=itemView.findViewById(R.id.item_title);
        }
    }
}
