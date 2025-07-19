import React, { useState, useEffect } from 'react';
import { Layout, Menu, InputNumber, Row, Col, message, Button, Dropdown, Space } from 'antd';
import {
  PieChartOutlined,
  GlobalOutlined,
  LineChartOutlined,
  DotChartOutlined,
  UserOutlined,
  LogoutOutlined,
} from '@ant-design/icons';
import TypePieChart from './components/TypePieChart';
import RegionPieChart from './components/RegionPieChart';
import ReleaseLineChart from './components/ReleaseLineChart';
import ScoreScatterChart from './components/ScoreScatterChart';
import ActorBarChart from './components/ActorBarChart';
import Login from './pages/Login';
import Register from './pages/Register';
import axios from 'axios';

const { Header, Sider, Content } = Layout;

const menuItems = [
  { key: 'type', icon: <PieChartOutlined />, label: '类型分布' },
  { key: 'region', icon: <GlobalOutlined />, label: '地区分布' },
  { key: 'release', icon: <LineChartOutlined />, label: '上映时间分布' },
  { key: 'score', icon: <DotChartOutlined />, label: '评分分布' },
  { key: 'actor', icon: <UserOutlined />, label: '演员热度' },
];

const App: React.FC = () => {
  const [collapsed, setCollapsed] = useState(false);
  const [selectedMenu, setSelectedMenu] = useState('type');
  const [rankMin, setRankMin] = useState(1);
  const [rankMax, setRankMax] = useState(100);
  
  // 用户状态
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [currentView, setCurrentView] = useState<'login' | 'register' | 'dashboard'>('login');
  const [username, setUsername] = useState('');
  const [token, setToken] = useState('');

  // 检查登录状态
  useEffect(() => {
    const savedToken = localStorage.getItem('token');
    const savedUsername = localStorage.getItem('username');
    
    if (savedToken && savedUsername) {
      setToken(savedToken);
      setUsername(savedUsername);
      setIsLoggedIn(true);
      setCurrentView('dashboard');
      
      // 设置axios默认headers
      axios.defaults.headers.common['Authorization'] = `Bearer ${savedToken}`;
    }
  }, []);

  // 登录成功处理
  const handleLoginSuccess = (newToken: string, newUsername: string) => {
    setToken(newToken);
    setUsername(newUsername);
    setIsLoggedIn(true);
    setCurrentView('dashboard');
    axios.defaults.headers.common['Authorization'] = `Bearer ${newToken}`;
  };

  // 注册成功处理
  const handleRegisterSuccess = () => {
    setCurrentView('login');
    message.info('注册成功，请登录');
  };

  // 登出处理
  const handleLogout = async () => {
    try {
      await axios.post('/api/logout');
    } catch (error) {
      // 即使登出请求失败，也要清除本地状态
    } finally {
      localStorage.removeItem('token');
      localStorage.removeItem('username');
      delete axios.defaults.headers.common['Authorization'];
      setIsLoggedIn(false);
      setToken('');
      setUsername('');
      setCurrentView('login');
      message.success('已登出');
    }
  };

  // 切换菜单
  const handleMenuClick = (e: any) => {
    setSelectedMenu(e.key);
  };

  // rank输入校验
  const handleRankChange = (type: 'min' | 'max', value: number | null) => {
    if (value === null) return;
    if (type === 'min') {
      if (value > rankMax) {
        message.error('最小rank不能大于最大rank');
        return;
      }
      setRankMin(value);
    } else {
      if (value < rankMin) {
        message.error('最大rank不能小于最小rank');
        return;
      }
      setRankMax(value);
    }
  };

  // 渲染内容区
  const renderContent = () => {
    switch (selectedMenu) {
      case 'type':
        return <TypePieChart rankMin={rankMin} rankMax={rankMax} />;
      case 'region':
        return <RegionPieChart rankMin={rankMin} rankMax={rankMax} />;
      case 'release':
        return <ReleaseLineChart rankMin={rankMin} rankMax={rankMax} />;
      case 'score':
        return <ScoreScatterChart rankMin={rankMin} rankMax={rankMax} />;
      case 'actor':
        return <ActorBarChart rankMin={rankMin} rankMax={rankMax} />;
      default:
        return null;
    }
  };

  // 用户下拉菜单
  const userMenuItems = [
    {
      key: 'logout',
      icon: <LogoutOutlined />,
      label: '登出',
      onClick: handleLogout,
    },
  ];

  // 如果未登录，显示登录或注册页面
  if (!isLoggedIn) {
    if (currentView === 'login') {
      return (
        <Login 
          onLoginSuccess={handleLoginSuccess}
          onSwitchToRegister={() => setCurrentView('register')}
        />
      );
    } else {
      return (
        <Register 
          onRegisterSuccess={handleRegisterSuccess}
          onSwitchToLogin={() => setCurrentView('login')}
        />
      );
    }
  }

  // 已登录，显示主界面
  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider collapsible collapsed={collapsed} onCollapse={setCollapsed}>
        <div style={{ height: 32, margin: 16, color: '#fff', textAlign: 'center', fontWeight: 'bold' }}>
          豆瓣电影Hot100
        </div>
        <Menu theme="dark" mode="inline" selectedKeys={[selectedMenu]} onClick={handleMenuClick} items={menuItems} />
      </Sider>
      <Layout>
        <Header style={{ background: '#fff', padding: '0 24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Row align="middle" gutter={16}>
            <Col>Rank范围：</Col>
            <Col>
              <InputNumber min={1} max={100} value={rankMin} onChange={v => handleRankChange('min', v)} />
            </Col>
            <Col>-</Col>
            <Col>
              <InputNumber min={1} max={100} value={rankMax} onChange={v => handleRankChange('max', v)} />
            </Col>
          </Row>
          
          <Dropdown menu={{ items: userMenuItems }} placement="bottomRight">
            <Button type="text" style={{ display: 'flex', alignItems: 'center' }}>
              <Space>
                <UserOutlined />
                {username}
              </Space>
            </Button>
          </Dropdown>
        </Header>
        <Content style={{ margin: '24px', background: '#fff', padding: 24, minHeight: 360 }}>
          {renderContent()}
        </Content>
      </Layout>
    </Layout>
  );
};

export default App; 
