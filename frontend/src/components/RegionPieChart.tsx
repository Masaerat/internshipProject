import React, { useEffect, useState } from 'react';
import axios from 'axios';
import ReactECharts from 'echarts-for-react';
import { Spin, Alert } from 'antd';

interface RegionPieChartProps {
  rankMin: number;
  rankMax: number;
}

interface RegionData {
  region: string;
  count: number;
}

const RegionPieChart: React.FC<RegionPieChartProps> = ({ rankMin, rankMax }) => {
  const [data, setData] = useState<RegionData[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    axios
      .get('/api/region-distribution', {
        params: { rank_min: rankMin, rank_max: rankMax },
      })
      .then((res) => {
        if (res.data.success) {
          setData(res.data.data);
        } else {
          setError(res.data.msg || '数据获取失败');
        }
      })
      .catch((err) => {
        setError(err.message || '请求失败');
      })
      .finally(() => setLoading(false));
  }, [rankMin, rankMax]);

  const option = {
    title: {
      text: '地区分布',
      left: 'center',
    },
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)',
    },
    legend: {
      orient: 'vertical',
      left: 'left',
    },
    series: [
      {
        name: '地区',
        type: 'pie',
        radius: '60%',
        data: data.map((item) => ({ name: item.region, value: item.count })),
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)',
          },
        },
      },
    ],
  };

  if (loading) return <Spin tip="加载中..." />;
  if (error) return <Alert type="error" message={error} />;
  return <ReactECharts option={option} style={{ height: 400 }} />;
};

export default RegionPieChart;
