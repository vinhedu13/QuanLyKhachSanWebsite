document.addEventListener('DOMContentLoaded', () => {
    const guestInput = document.getElementById('guests');
    const guestDropdown = document.querySelector('.guest-dropdown');
    const applyButton = document.querySelector('.apply-btn');

    // Toggle dropdown visibility
    guestInput.addEventListener('click', () => {
        guestDropdown.style.display = guestDropdown.style.display === 'block' ? 'none' : 'block';
    });

    // Handle increase and decrease buttons
    document.querySelectorAll('.increase, .decrease').forEach(button => {
        button.addEventListener('click', (e) => {
            const target = e.target.getAttribute('data-target');
            const countSpan = document.getElementById(`${target}-count`);
            let currentValue = parseInt(countSpan.textContent, 10);

            if (e.target.classList.contains('increase')) {
                currentValue++;
            } else if (currentValue > 0) {
                currentValue--;
            }

            countSpan.textContent = currentValue;
        });
    });

    // Apply selected values
    applyButton.addEventListener('click', () => {
        const adults = document.getElementById('adults-count').textContent;

        guestInput.value = `${adults}`;
        guestDropdown.style.display = 'none';
    });

    // Close dropdown if clicked outside
    document.addEventListener('click', (e) => {
        if (!document.getElementById('guest-picker').contains(e.target)) {
            guestDropdown.style.display = 'none';
        }
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const discountForm = document.getElementById('discount-form');
    const discountCodeInput = document.getElementById('discount-code');
    const discountMessage = document.getElementById('discount-message');

    const validCodes = {
        SALE20: 'Bạn đã áp dụng thành công giảm giá 20%!',
        FREESHIP: 'Bạn đã áp dụng thành công miễn phí vận chuyển!',
        TECH10: 'Bạn đã áp dụng thành công giảm giá 10% cho sản phẩm công nghệ!',
    };

    discountForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const code = discountCodeInput.value.trim().toUpperCase();

        if (validCodes[code]) {
            discountMessage.textContent = validCodes[code];
            discountMessage.classList.remove('hidden');
            discountMessage.style.color = 'green';
        } else {
            discountMessage.textContent = 'Mã giảm giá không hợp lệ. Vui lòng thử lại.';
            discountMessage.classList.remove('hidden');
            discountMessage.style.color = 'red';
        }

        discountCodeInput.value = '';
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const searchForm = document.getElementById('search-form');
    const resultsTable = document.getElementById('results-table').getElementsByTagName('tbody')[0];
    const noResultsMessage = document.createElement('div'); // Tạo phần tử div cho thông báo

    noResultsMessage.classList.add('alert', 'alert-danger'); // Thêm lớp Bootstrap alert-danger
    noResultsMessage.style.display = 'none'; // Ẩn thông báo ban đầu

    noResultsMessage.textContent = 'Không có đơn hàng nào được tìm thấy'; // Nội dung thông báo

    const sampleOrders = [
        {id: 'ORD001', date: '2024-11-10', status: 'Đang xử lý', value: '500,000 VND'},
        {id: 'ORD002', date: '2024-11-12', status: 'Đã giao', value: '1,200,000 VND'},
        {id: 'ORD003', date: '2024-11-13', status: 'Đã hủy', value: '300,000 VND'},
        {id: 'ORD004', date: '2024-11-14', status: 'Đang xử lý', value: '700,000 VND'}
    ];

    // Hàm lọc đơn hàng theo thông tin nhập vào
    function filterOrders(orderId, orderDate) {
        return sampleOrders.filter(order => {
            const matchesId = orderId ? order.id.includes(orderId) : true;
            const matchesDate = orderDate ? order.date === orderDate : true;
            return matchesId && matchesDate;
        });
    }

    // Hàm hiển thị kết quả tìm kiếm lên bảng
    function displayResults(orders) {
        resultsTable.innerHTML = ''; // Xóa bảng trước khi hiển thị kết quả mới
        if (orders.length === 0) {
            resultsTable.parentElement.appendChild(noResultsMessage); // Thêm thông báo vào container
            noResultsMessage.style.display = 'block'; // Hiển thị thông báo
        } else {
            noResultsMessage.style.display = 'none'; // Ẩn thông báo
            orders.forEach(order => {
                const row = resultsTable.insertRow();
                row.insertCell(0).textContent = order.id;
                row.insertCell(1).textContent = order.date;
                row.insertCell(2).textContent = order.status;
                row.insertCell(3).textContent = order.value;
            });
        }
    }

    // Xử lý khi form tìm kiếm được gửi
    searchForm.addEventListener('submit', (event) => {
        event.preventDefault();

        const orderId = document.getElementById('order-id').value.trim();
        const orderDate = document.getElementById('order-date').value.trim();


        const filteredOrders = filterOrders(orderId, orderDate);
        displayResults(filteredOrders);
    });
});
document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('container')
    const registerBtn = document.getElementById('register')
    const loginBtn = document.getElementById('login')

    registerBtn.addEventListener('click', () => {
        container.classList.add("active");
    })

    loginBtn.addEventListener('click', () => {
        container.classList.remove('active');
    })
});

document.addEventListener('DOMContentLoaded', () => {
    const promoTimer = document.getElementById('promo-timer');

    // Thời gian kết thúc khuyến mãi (tùy chỉnh thời gian)
    const promoEndTime = new Date();
    promoEndTime.setMinutes(promoEndTime.getMinutes() + 30); // Khuyến mãi kết thúc sau 30 phút

    // Hàm đếm ngược
    function updateTimer() {
        const now = new Date();
        const timeLeft = promoEndTime - now;

        if (timeLeft <= 0) {
            promoTimer.textContent = "Hết thời gian!";
            clearInterval(timerInterval);
            return;
        }

        const minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);
        promoTimer.textContent = `${minutes} phút ${seconds} giây`;
    }

    // Cập nhật mỗi giây
    updateTimer();
    const timerInterval = setInterval(updateTimer, 1000);
});


function updateMaxCustomers(luongKhachToiDa) {
    // Tính số phòng được chọn
    const selectedRooms = document.querySelectorAll('.form-check-input:checked').length;

    // Lấy giới hạn khách tối đa trên mỗi phòng
    const maxCustomersPerRoom = luongKhachToiDa;

    // Tính tổng số khách tối đa
    const maxCustomers = selectedRooms * maxCustomersPerRoom;

    // Hiện hoặc xóa bớt khách hàng nếu cần
    const customerList = document.querySelectorAll('[id^="label"]');
    if (customerList.length > maxCustomers) {
        for (let i = customerList.length; i > maxCustomers; i--) {
            deleteHTMLCustomer(i); // Gọi hàm xóa khách hàng
        }
    }
    return maxCustomers
}

function deleteHTMLCustomer(field) {
    const label = document.getElementById(`label${field}`);
    if (label) {
        label.parentElement.remove(); // Xóa toàn bộ phần tử li của khách hàng
    }
}


function submitForm() {
    document.getElementById('formLoaiPhong').submit(); // Tự động gửi form
}

function collectFormData() {
    // Lấy giá trị từ dropdown idLoaiPhong
    const idLoaiPhong = document.querySelector('[name="idLoaiPhong"]').value;
    document.getElementById('hiddenIdLoaiPhong').value = idLoaiPhong;

    // Lấy giá trị từ input datetime-local ngayTraPhong
    const ngayTraPhong = document.querySelector('[name="ngayTraPhong"]').value;
    document.getElementById('hiddenNgayTraPhong').value = ngayTraPhong;

    // Lấy danh sách phòng được chọn
    const phongDuocChon = Array.from(document.querySelectorAll('.form-check-input:checked'))
        .map(input => input.nextElementSibling.innerText.trim())
        .join(', ');
    document.getElementById('hiddenPhongDuocChon').value = phongDuocChon;

    // Lấy tất cả các span của khách hàng
    const khachHang = Array.from(document.querySelectorAll('[id^="span-customer-"]'))
        .map(label => label.innerText.trim())
        .filter(text => !text.startsWith('Khách hàng ')) // Loại bỏ các khách hàng chưa được nhập thông tin
        .join('; ');
    document.getElementById('hiddenKhachHang').value = khachHang;

    // Tạo map giá theo idLoaiPhong
    const priceMap = {
        "1": 500000, // Ví dụ idLoaiPhong = 1 có giá 500.000
        "2": 800000, // Ví dụ idLoaiPhong = 2 có giá 800.000
        "3": 1200000 // Ví dụ idLoaiPhong = 3 có giá 1.200.000
    };

    // Tính tổng tiền
    const donGia = priceMap[idLoaiPhong] || 0; // Lấy đơn giá, nếu không có thì giá mặc định là 0
    const soLuongPhong = phongDuocChon.length; // Số lượng phòng được chọn
    const tongTien = donGia * soLuongPhong;

    // Gán tổng tiền vào thẻ ẩn
    document.getElementById('hiddenTongTien').value = tongTien;


}

function submitMainForm() {
    if (validateForm()) {
        collectFormData(); // Thu thập dữ liệu trước khi submit
        document.getElementById('mainForm').submit();
    }
}

function validateForm() {
    // Kiểm tra dropdown idLoaiPhong
    const idLoaiPhong = document.querySelector('[name="idLoaiPhong"]').value;
    if (!idLoaiPhong) {
        alert('Vui lòng chọn loại phòng.');
        return false;
    }

    // Kiểm tra input datetime-local ngayTraPhong
    const ngayTraPhong = document.querySelector('[name="ngayTraPhong"]').value;
    if (!ngayTraPhong) {
        alert('Vui lòng chọn ngày trả phòng.');
        return false;
    }

    // Kiểm tra ít nhất một phòng được chọn
    const phongDuocChon = document.querySelectorAll('.form-check-input:checked');
    if (phongDuocChon.length === 0) {
        alert('Vui lòng chọn ít nhất một phòng.');
        return false;
    }

    // Kiểm tra ít nhất một khách hàng đã được nhập thông tin
    const khachHang = Array.from(document.querySelectorAll('[id^="span-customer-"]'))
        .some(label => !label.innerText.startsWith('Khách hàng '));
    if (!khachHang) {
        alert('Vui lòng nhập thông tin cho ít nhất một khách hàng.');
        return false;
    }

    return true; // Tất cả đều hợp lệ
}

const roomCustomerData = {}; // Lưu trữ khách hàng theo phòng

// Tạo hoặc cập nhật danh sách khách hàng cho từng phòng
function updateCustomerSection(luongKhachToiDa) {
    const selectedRooms = document.querySelectorAll('.form-check-input:checked');
    const customerSection = document.getElementById('customer-section');

    // Xóa các danh sách cũ
    customerSection.innerHTML = '';

    // Tạo danh sách khách hàng cho từng phòng được chọn
    selectedRooms.forEach((room) => {
        const roomId = room.value;

        // Khởi tạo dữ liệu khách hàng nếu chưa tồn tại
        if (!roomCustomerData[roomId]) {
            roomCustomerData[roomId] = [];
        }

        // Tạo div riêng cho mỗi phòng
        const roomDiv = document.createElement('div');
        roomDiv.className = 'mb-4';
        roomDiv.id = `room-customers-${roomId}`;
        roomDiv.innerHTML = `
                <h6 class="text-secondary">Phòng ${roomId}</h6>
                <ul class="list-unstyled" id="customer-list-${roomId}">
                    ${roomCustomerData[roomId].map((_, index) => generateCustomerHTML(roomId, index + 1)).join('')}
                </ul>
                <button class="btn btn-primary btn-sm mt-2" onclick="addCustomer(${luongKhachToiDa}, ${roomId})">
                    Thêm Khách Hàng
                </button>
            `;
        customerSection.appendChild(roomDiv);
    });
}

// Thêm khách hàng vào danh sách của một phòng
function addCustomer(luongKhachToiDa, roomId) {
    const currentCustomers = roomCustomerData[roomId] || [];

    if (currentCustomers.length < luongKhachToiDa) {
        const newCustomerIndex = currentCustomers.length + 1;
        currentCustomers.push(`Khách hàng ${newCustomerIndex}`);

        const customerList = document.getElementById(`customer-list-${roomId}`);
        const newCustomerItem = document.createElement('li');
        // newCustomerItem.className = 'mb-3 d-flex align-items-center justify-content-between';
        // newCustomerItem.id = `customer-${roomId}-${newCustomerIndex}`;
        newCustomerItem.innerHTML = generateCustomerHTML(roomId, newCustomerIndex);

        customerList.appendChild(newCustomerItem);
    } else {
        alert(`Không thể thêm quá ${luongKhachToiDa} khách hàng vào phòng này!`);
    }
}

// Xóa khách hàng
function deleteCustomer(roomId, customerIndex) {
    // Xóa khách hàng khỏi dữ liệu
    if (roomCustomerData[roomId]) {
        roomCustomerData[roomId].splice(customerIndex - 1, 1);
    }

    // Lấy danh sách khách hàng hiện tại
    const customerList = document.getElementById(`customer-list-${roomId}`);

    // Làm mới giao diện danh sách khách hàng
    customerList.innerHTML = roomCustomerData[roomId]
        .map((_, index) => generateCustomerHTML(roomId, index + 1)) // Tạo lại danh sách với chỉ mục chính xác
        .join('');
}


// Tạo HTML cho khách hàng
function generateCustomerHTML(roomId, customerIndex) {
    return `
            <li class="mb-3 d-flex align-items-center justify-content-between" id="customer-${roomId}-${customerIndex}">
                <span id="span-customer-${roomId}-${customerIndex}">Khách hàng ${customerIndex}</span>
                <div>
                    <button class="btn btn-outline-primary btn-sm" onclick="openPopup(${roomId}, ${customerIndex})">Nhập Thông Tin</button>
                    <button class="btn btn-outline-danger btn-sm ms-2" onclick="deleteCustomer(${roomId}, ${customerIndex})">Xóa</button>
                </div>
            </li>
        `;
}

// Lắng nghe sự kiện thay đổi phòng
document.querySelectorAll('.form-check-input').forEach(input => {
    input.addEventListener('change', () => {
        const maxCustomersPerRoom = 3; // Ví dụ số khách tối đa mỗi phòng
        updateCustomerSection(maxCustomersPerRoom);
    });
});

// // Hàm submit dữ liệu khách hàng
// function submitCustomerData() {
//     const customerData = Object.entries(roomCustomerData).map(([roomId, customers]) => {
//         return {
//             roomId: roomId,
//             customers: customers.map((customer, index) => ({
//                 name: customer,
//                 index: index + 1
//             }))
//         };
//     });
//
//     // Gửi dữ liệu đến server
//     fetch('/submit-customers', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify(customerData)
//     })
//         .then(response => {
//             if (response.ok) {
//                 alert('Dữ liệu khách hàng đã được gửi thành công!');
//             } else {
//                 alert('Đã xảy ra lỗi khi gửi dữ liệu.');
//             }
//         })
//         .catch(error => {
//             console.error('Lỗi:', error);
//             alert('Đã xảy ra lỗi khi gửi dữ liệu.');
//         });
// }

// Tạo biến toàn cục để lưu thông tin trường hiện tại
let currentField = null;

// Mở popup và điền dữ liệu nếu có
function openPopup(roomId, customerIndex) {
    currentField = {roomId, customerIndex}; // Lưu trữ thông tin hiện tại

    // Lấy dữ liệu khách hàng hiện tại
    const customerData = roomCustomerData[roomId] && roomCustomerData[roomId][customerIndex - 1];
    document.getElementById('popupForm').reset();

    // Mở modal
    const modal = new bootstrap.Modal(document.getElementById('inputModal'));
    modal.show();
}

// Hàm lưu dữ liệu
function saveData() {
    // Lấy giá trị từ các trường nhập liệu
    const fullName = document.getElementById('fullName').value.trim();
    const identityCard = document.getElementById('identityCard').value.trim();
    const loaiKhach = document.getElementById('loaiKhach').value;

    // Kiểm tra tính hợp lệ của các trường
    if (fullName && identityCard && loaiKhach) {
        const {roomId, customerIndex} = currentField; // Lấy thông tin phòng và chỉ số khách hàng

        // Cập nhật dữ liệu khách hàng
        roomCustomerData[roomId][customerIndex - 1] = `${fullName} - ${identityCard} - ${loaiKhach}`;

        // Cập nhật nhãn của khách hàng trong danh sách
        const targetLabel = document.getElementById(`span-customer-${roomId}-${customerIndex}`);
        if (targetLabel) {
            targetLabel.innerText = `${fullName} (${identityCard}) - ${loaiKhach} - ${roomId}`;
        }
        // Đóng modal
        const modal = bootstrap.Modal.getInstance(document.getElementById('inputModal'));
        if (modal) {
            modal.hide();
        }
    } else {
        alert('Vui lòng nhập đầy đủ thông tin!');
    }
}
